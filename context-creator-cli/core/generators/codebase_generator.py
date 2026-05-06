import os
import json
import tempfile
import urllib.parse
import subprocess
from pathlib import Path
from core.constants import IGNORED_DIRS, IGNORED_FILES, IGNORED_EXTENSIONS, EXT_TO_LANG, PROMPT_PACK_TEMPLATES
from .token_manager import TokenManager
from .file_processor import FileProcessor
from .artifacts import ArtifactGenerator
from .git_manager import GitManager

class CodebaseGenerator:
    def __init__(self, config, cancel_event, log_cb, progress_cb, complete_cb):
        self.config = config
        self.cancel_event = cancel_event
        self.log = log_cb
        self.progress = progress_cb
        self.complete = complete_cb
        self.token_manager = TokenManager(config, log_cb)
        self.file_processor = FileProcessor(config)
        self.artifacts = ArtifactGenerator()
        self.git_manager = GitManager(log_cb)

    def run(self):
        temp_dir_obj = None
        success = False
        payload = {}
        try:
            filename = self.config['output_file'] or "my_project.md"
            opt_mode = self.config.get('llm_opt', 'ChatGPT / Standard (Markdown)')
            if opt_mode == 'JSON Structured Export' and not filename.endswith('.json'):
                filename = f"{Path(filename).stem}.json"
            out_filepath = Path(self.config['output_dir']) / filename

            try: max_size_bytes = float(self.config['max_size_kb'] or 0) * 1024
            except ValueError: max_size_bytes = float('inf')
            try: max_lines = int(self.config['max_lines'] or 0)
            except ValueError: max_lines = float('inf')

            allowed_exts =[e.strip() if e.strip().startswith('.') else f".{e.strip()}" for e in self.config['extensions'].split(',') if e.strip()]
            custom_ignores = {d.strip() for d in self.config['custom_ignores'].split(',') if d.strip()}
            active_ignored_dirs = IGNORED_DIRS.union(custom_ignores)

            if self.config['mode'] == 'local':
                root_path = Path(self.config['input_dir'])
                project_name = root_path.name
            elif self.config['mode'] == 'remote':
                repo_url = self.config['repo_url']
                auth_token = self.config.get('pat', '')
                project_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
                self.log(f"Cloning remote repository '{project_name}' (--depth 1)...")
                
                temp_dir_obj = tempfile.TemporaryDirectory()
                clone_path = temp_dir_obj.name
                clone_url = repo_url
                if auth_token:
                    parsed = urllib.parse.urlparse(repo_url)
                    if parsed.scheme in ('http', 'https'):
                        host = parsed.netloc.split('@')[-1]
                        clone_url = parsed._replace(netloc=f"{urllib.parse.quote(auth_token, safe='')}@{host}").geturl()
                try:
                    subprocess.run(["git", "clone", "--depth", "1", clone_url, clone_path], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    raise Exception(f"Git clone failed: {e.stderr.replace(auth_token, '***') if auth_token else e.stderr}")
                root_path = Path(clone_path)

            gitignore_patterns = self.git_manager.parse_gitignore(root_path) if self.config['use_gitignore'] else []
            valid_files, deps_dict, found_langs =[], {}, set()
            generate_tech_stack = self.config['generate_tech_stack']

            self.log("Phase 1: Scanning directories & applying filters...")
            for dirpath, dirnames, filenames in os.walk(root_path):
                if self.cancel_event.is_set(): return self.log("Cancelled.")
                dirnames[:] =[d for d in dirnames if d not in active_ignored_dirs]
                for file in filenames:
                    full_path = Path(dirpath) / file
                    if full_path.is_symlink(): continue
                    if generate_tech_stack and file in['package.json', 'requirements.txt']:
                        self.artifacts.parse_deps(full_path, file, deps_dict)
                    if file in IGNORED_FILES: continue
                    if allowed_exts and not any(file.endswith(ext) for ext in allowed_exts): continue
                    elif not allowed_exts and (file.startswith('.env') or any(file.endswith(ext) for ext in IGNORED_EXTENSIONS)): continue
                    if gitignore_patterns and self.git_manager.is_ignored_by_gitignore(full_path, root_path, gitignore_patterns): continue
                    
                    try:
                        if max_size_bytes and full_path.stat().st_size > max_size_bytes: continue
                    except OSError: continue
                    if self.file_processor.is_binary_file(full_path): continue
                    valid_files.append(full_path)

            if not valid_files:
                return self.log("No valid files found matching criteria.")

            git_mode = self.config.get('git_mode', 'All Files')
            if git_mode != 'All Files' and self.config['mode'] != 'remote':
                self.log(f"Applying Git Filter: {git_mode}...")
                changed_files = self.git_manager.get_changed_files(root_path, git_mode)
                if changed_files is not None:
                    valid_files =[f for f in valid_files if f.resolve() in changed_files]
                    self.log(f"Git filter reduced selection to {len(valid_files)} files.")

            rel_paths =[p.relative_to(root_path) for p in valid_files]
            tree_str = f"{project_name}/\n" + self.artifacts.build_ascii_tree(rel_paths)

            self.log("Phase 2: Processing, Scoring & Summarizing files...")
            processed_files =[]
            secret_scan = self.config.get('secret_scan', False)
            summaries = self.config.get('summaries', False)
            total_files = len(valid_files)

            for i, path in enumerate(valid_files):
                if self.cancel_event.is_set(): return self.log("Cancelled.")
                self.progress((i / total_files) * 40) 
                rel_path = path.relative_to(root_path)
                ext = path.suffix.lower()
                if generate_tech_stack and ext in EXT_TO_LANG: found_langs.add(EXT_TO_LANG[ext])
                
                try:
                    with open(path, 'r', encoding='utf-8') as src_file:
                        original_content = src_file.read()
                except Exception: continue
                
                content = self.file_processor.apply_formatting(original_content, ext)
                if max_lines and len(content.splitlines()) > max_lines:
                    content = "\n".join(content.splitlines()[:max_lines]) + f"\n\n// Truncated: Exceeds {max_lines} lines limit."
                
                if secret_scan:
                    content, scount = self.file_processor.redact_secrets(content)
                    if scount > 0: self.log(f"Redacted {scount} secret(s) in {rel_path}")
                
                summary_text = self.file_processor.generate_summary(path, original_content) if summaries else ""
                tokens = self.token_manager.count_tokens(content + summary_text + str(rel_path))
                
                processed_files.append({
                    'path': path, 'rel_path': rel_path, 'content': content,
                    'summary': summary_text, 'tokens': tokens, 
                    'score': self.file_processor.calculate_score(path, root_path), 
                    'ext': ext.lstrip('.')
                })

            self.log("Phase 3: Applying AI Output Optimizations...")
            processed_files.sort(key=lambda x: x['score'], reverse=True)
            budget = self.token_manager.get_token_budget()
            final_files =[]
            current_tokens = self.token_manager.count_tokens(tree_str)

            for fd in processed_files:
                if budget > 0 and (current_tokens + fd['tokens'] > budget):
                    fd['content'] = f"// File excluded to fit within {budget} token budget.\n// Content length was ~{fd['tokens']} tokens."
                    fd['tokens'] = self.token_manager.count_tokens(fd['content'])
                    if current_tokens + fd['tokens'] <= budget:
                        final_files.append(fd)
                        current_tokens += fd['tokens']
                else:
                    final_files.append(fd)
                    current_tokens += fd['tokens']

            final_files.sort(key=lambda x: str(x['rel_path']))

            self.log(f"Phase 4: Writing Final Context Package in[{opt_mode}] format...")
            if opt_mode == 'JSON Structured Export':
                json_data = {
                    "repository": project_name,
                    "folder_structure": tree_str,
                    "documents":[]
                }
                for i, fd in enumerate(final_files):
                    self.progress(40 + (i / len(final_files)) * 40)
                    json_data["documents"].append({
                        "path": str(fd["rel_path"]),
                        "extension": fd["ext"],
                        "summary": fd["summary"].strip() if fd["summary"] else None,
                        "content": fd["content"]
                    })
                with open(out_filepath, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2)
            else:
                with open(out_filepath, 'w', encoding='utf-8') as f:
                    if opt_mode == 'Claude Optimized (XML)':
                        f.write(f"<!-- Repository Context for: {project_name} -->\n\n<repository_structure>\n<![CDATA[\n{tree_str}\n]]>\n</repository_structure>\n\n<documents>\n")
                    elif opt_mode == 'Gemini Optimized (Delimited)':
                        f.write(f"# Codebase: {project_name}\n\n## Folder Structure\n```text\n{tree_str}\n```\n\n## Code Files\n\n")
                    elif opt_mode == 'Raw Text':
                        f.write(f"Repository: {project_name}\n\nStructure:\n{tree_str}\n\nFiles:\n\n")
                    else:
                        f.write(f"# Codebase Context: {project_name}\n\n## Project Structure\n\n```text\n{tree_str}\n```\n\n## File Contents\n\n")
                    
                    for i, fd in enumerate(final_files):
                        if self.cancel_event.is_set(): return self.log("Cancelled.")
                        self.progress(40 + (i / len(final_files)) * 40)
                        if opt_mode == 'Claude Optimized (XML)':
                            f.write(f'<document index="{i+1}">\n<source>{fd["rel_path"]}</source>\n')
                            if fd["summary"]: f.write(f'<summary>\n{fd["summary"]}</summary>\n')
                            f.write(f'<document_content>\n{fd["content"]}\n</document_content>\n</document>\n\n')
                        elif opt_mode == 'Gemini Optimized (Delimited)':
                            f.write(f"================================================================================\nFile: {fd['rel_path']}\n================================================================================\n")
                            if fd["summary"]: f.write(fd["summary"])
                            f.write(f"```{fd['ext']}\n{fd['content']}\n```\n\n")
                        elif opt_mode == 'Raw Text':
                            f.write(f"--- File: {fd['rel_path']} ---\n")
                            if fd["summary"]: f.write(f"Summary:\n{fd['summary']}\n")
                            f.write(f"{fd['content']}\n\n")
                        else:
                            f.write(f"### `{fd['rel_path']}`\n\n")
                            if fd["summary"]: f.write(fd["summary"])
                            f.write(f"```{fd['ext']}\n{fd['content']}\n```\n\n")
                    
                    if opt_mode == 'Claude Optimized (XML)': f.write("</documents>\n")

            self.log("Phase 5: Generating Extra Artifacts...")
            out_dir = Path(self.config['output_dir'])
            base_name = Path(filename).stem
            
            if generate_tech_stack:
                deps_filepath = out_dir / f"{base_name}_tech_stack.md"
                with open(deps_filepath, 'w', encoding='utf-8') as df:
                    df.write(f"# Tech Stack & Dependencies: {project_name}\n\n## 💻 Languages Used\n")
                    df.writelines([f"- {l}\n" for l in sorted(found_langs)] if found_langs else "No standard languages recognized.\n")
                    df.write("\n## 📦 Dependencies\n")
                    for source, pkgs in sorted(deps_dict.items()):
                        df.write(f"\n### {source}\n")
                        for pkg in sorted(pkgs): df.write(f"- `{pkg}`\n")
            
            if self.config.get('mermaid_graph'):
                mermaid_filepath = out_dir / f"{base_name}_dependency_graph.md"
                mermaid_str = self.artifacts.build_mermaid_graph(rel_paths, project_name)
                with open(mermaid_filepath, 'w', encoding='utf-8') as mf:
                    mf.write(f"# File Structure Graph: {project_name}\n\n```mermaid\n{mermaid_str}\n```\n")
            
            if self.config.get('prompt_packs'):
                prompts_filepath = out_dir / f"{base_name}_prompts.md"
                with open(prompts_filepath, 'w', encoding='utf-8') as pf:
                    pf.write(f"# Prompt Pack for {project_name}\n\n*Copy and paste these along with your codebase context to get started quickly.*\n\n")
                    for title, prompt in PROMPT_PACK_TEMPLATES:
                        pf.write(f"### {title}\n```text\n{prompt}\n```\n\n")

            self.progress(100)
            self.log(f"\nSuccess! Primary context file saved to:\n{out_filepath}\nEstimated Total Context Size: ~{current_tokens:,} tokens")
            
            clipboard_text = None
            if self.config.get('clipboard_mode'):
                self.log("Loading generated text into clipboard memory...")
                try:
                    with open(out_filepath, 'r', encoding='utf-8') as f:
                        clipboard_text = f.read()
                except Exception as e:
                    self.log(f"Warning: Failed to load clipboard text: {e}")
            
            payload = {
                "filepath": str(out_filepath),
                "copy_clipboard": self.config.get('clipboard_mode', False),
                "clipboard_text": clipboard_text
            }
            success = True

        except Exception as e:
            self.log(f"\nCRITICAL ERROR: {str(e)}")
        finally:
            if temp_dir_obj:
                try: temp_dir_obj.cleanup()
                except Exception as e: self.log(f"Warning: Failed to clear temporary directory: {e}")
            self.complete(success, payload)