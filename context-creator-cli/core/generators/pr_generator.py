import json
import tempfile
import urllib.parse
import urllib.request
import subprocess
import re
from pathlib import Path
from .token_manager import TokenManager
from .file_processor import FileProcessor

class PRGenerator:
    def __init__(self, config, cancel_event, log_cb, progress_cb, complete_cb):
        self.config = config
        self.cancel_event = cancel_event
        self.log = log_cb
        self.progress = progress_cb
        self.complete = complete_cb
        self.token_manager = TokenManager(config, log_cb)
        self.file_processor = FileProcessor(config)

    def run(self):
        pr_url = self.config['pr_url'].strip()
        pat = self.config.get('pat', '').strip()
        is_github = 'github.com' in pr_url
        is_gitlab = 'gitlab.com' in pr_url

        if not is_github and not is_gitlab:
            self.log("Error: PR URL must be from github.com or gitlab.com")
            self.complete(False)
            return

        self.log("Phase 1: Fetching Pull Request metadata from API...")
        headers = {'User-Agent': 'ContextCreator'}
        if pat:
            if is_github: headers['Authorization'] = f"token {pat}"
            elif is_gitlab: headers['PRIVATE-TOKEN'] = pat
            
        try:
            if is_github:
                match = re.search(r'github\.com/([^/]+)/([^/]+)/pull/(\d+)', pr_url)
                if not match: raise ValueError("Invalid GitHub PR URL format.")
                owner, repo, pr_id = match.groups()
                api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}"
                req = urllib.request.Request(api_url, headers=headers)
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                title = data.get('title', '')
                body = data.get('body', '')
                base_sha = data['base']['sha']
                head_sha = data['head']['sha']
                clone_url = data['base']['repo']['clone_url']
            elif is_gitlab:
                match = re.search(r'gitlab\.com/(.+?)/-/merge_requests/(\d+)', pr_url)
                if not match: raise ValueError("Invalid GitLab MR URL format.")
                project_path, mr_id = match.groups()
                project_path_encoded = urllib.parse.quote(project_path, safe='')
                api_url = f"https://gitlab.com/api/v4/projects/{project_path_encoded}/merge_requests/{mr_id}"
                req = urllib.request.Request(api_url, headers=headers)
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                title = data.get('title', '')
                body = data.get('description', '')
                base_sha = data.get('diff_refs', {}).get('base_sha')
                head_sha = data.get('diff_refs', {}).get('head_sha')
                clone_url = f"https://gitlab.com/{project_path}.git"
                if not base_sha or not head_sha:
                    raise ValueError("GitLab MR does not contain diff_refs. The MR might be empty.")
        except Exception as e:
            self.log(f"Error fetching API: {str(e)}")
            self.complete(False)
            return

        self.log(f"PR Title: {title}")
        self.log("Phase 2: Cloning repository to fetch changes...")
        temp_dir_obj = tempfile.TemporaryDirectory()
        clone_path = temp_dir_obj.name
        auth_clone_url = clone_url
        if pat:
            parsed = urllib.parse.urlparse(clone_url)
            if is_github:
                auth_clone_url = parsed._replace(netloc=f"{urllib.parse.quote(pat, safe='')}@{parsed.netloc}").geturl()
            elif is_gitlab:
                auth_clone_url = parsed._replace(netloc=f"oauth2:{urllib.parse.quote(pat, safe='')}@{parsed.netloc}").geturl()
                
        try:
            self.log("Cloning bare repository (fast index)...")
            subprocess.run(["git", "clone", "--bare", auth_clone_url, clone_path], check=True, capture_output=True, text=True)
            self.log("Fetching exact PR commits...")
            if is_github:
                subprocess.run(["git", "-C", clone_path, "fetch", "origin", f"pull/{pr_id}/head:pr_head"], check=True, capture_output=True, text=True)
            elif is_gitlab:
                subprocess.run(["git", "-C", clone_path, "fetch", "origin", f"refs/merge-requests/{mr_id}/head:pr_head"], check=True, capture_output=True, text=True)
            self.log("Calculating exact diff...")
            diff_cmd =["git", "-C", clone_path, "diff", "--name-status", base_sha, head_sha]
            diff_res = subprocess.run(diff_cmd, check=True, capture_output=True, text=True)
            changed_files = diff_res.stdout.splitlines()
        except subprocess.CalledProcessError as e:
            temp_dir_obj.cleanup()
            safe_err = e.stderr.replace(pat, '***') if pat else e.stderr
            self.log(f"Git operation failed: {safe_err}")
            self.complete(False)
            return

        self.log(f"Phase 3: Generating side-by-side comparison for {len(changed_files)} files...")
        filename = self.config['output_file'] or "pr_review.md"
        out_filepath = Path(self.config['output_dir']) / filename
        allowed_exts =[e.strip() if e.strip().startswith('.') else f".{e.strip()}" for e in self.config['extensions'].split(',') if e.strip()]
        
        budget = self.token_manager.get_token_budget()
        try: max_size_bytes = float(self.config['max_size_kb'] or 0) * 1024
        except ValueError: max_size_bytes = float('inf')
        try: max_lines = int(self.config['max_lines'] or 0)
        except ValueError: max_lines = float('inf')
        secret_scan = self.config.get('secret_scan', False)

        with open(out_filepath, 'w', encoding='utf-8') as f:
            header_text = (
                f"# PR Review Request: {title}\n\n"
                f"**System Prompt / Instructions:**\n"
                f"You are an expert code reviewer. Please review the following Pull Request. "
                f"I have provided the PR description and a side-by-side comparison of all changed files. "
                f"Please summarize the changes, identify any potential bugs, edge cases, or security issues, "
                f"and provide a final recommendation on whether this PR can/should be merged.\n\n"
                f"**PR URL:** {pr_url}\n\n"
                f"## PR Description\n{body or 'No description provided.'}\n\n"
                f"## File Changes\n\n"
            )
            f.write(header_text)
            current_tokens = self.token_manager.count_tokens(header_text)

            for i, line in enumerate(changed_files):
                if self.cancel_event.is_set():
                    self.log("Cancelled.")
                    temp_dir_obj.cleanup()
                    self.complete(False)
                    return
                if not line.strip(): continue
                self.progress((i / max(1, len(changed_files))) * 100)
                
                parts = line.split('\t')
                status = parts[0][0] 
                file_path = parts[2] if status == 'R' and len(parts) > 2 else parts[1]
                ext = Path(file_path).suffix.lower()
                
                if allowed_exts and not any(file_path.endswith(e) for e in allowed_exts):
                    continue

                def get_git_file(sha, path):
                    res = subprocess.run(["git", "-C", clone_path, "show", f"{sha}:{path}"], capture_output=True)
                    if res.returncode == 0:
                        try: return res.stdout.decode('utf-8')
                        except UnicodeDecodeError: return "// Binary file or non-UTF-8 content."
                    return None

                base_content = get_git_file(base_sha, file_path) if status != 'A' else "// File added in this PR."
                head_content = get_git_file(head_sha, file_path) if status != 'D' else "// File deleted in this PR."
                if base_content is None: base_content = "// File not found in base."
                if head_content is None: head_content = "// File not found in head."

                def process_content(c, extension):
                    if c is None or c.startswith("// File"): return c
                    return self.file_processor.apply_formatting(c, extension)

                base_content = process_content(base_content, ext)
                head_content = process_content(head_content, ext)

                if max_size_bytes and max_size_bytes > 0:
                    if len(base_content.encode('utf-8')) > max_size_bytes: base_content = f"// File exceeds maximum size limit of {max_size_bytes/1024} KB."
                    if len(head_content.encode('utf-8')) > max_size_bytes: head_content = f"// File exceeds maximum size limit of {max_size_bytes/1024} KB."
                if max_lines and max_lines > 0:
                    if len(base_content.splitlines()) > max_lines: base_content = "\n".join(base_content.splitlines()[:max_lines]) + f"\n\n// Truncated: Exceeds {max_lines} lines limit."
                    if len(head_content.splitlines()) > max_lines: head_content = "\n".join(head_content.splitlines()[:max_lines]) + f"\n\n// Truncated: Exceeds {max_lines} lines limit."

                if secret_scan:
                    base_content, _ = self.file_processor.redact_secrets(base_content)
                    head_content, _ = self.file_processor.redact_secrets(head_content)

                file_output = (
                    f"### `{file_path}`\n"
                    f"**Change Type:** {status}\n\n"
                    f"#### 🔴 Base Version (`{base_sha[:7]}`)\n"
                    f"```{ext.lstrip('.')}\n{base_content}\n```\n\n"
                    f"#### 🟢 PR Version (`{head_sha[:7]}`)\n"
                    f"```{ext.lstrip('.')}\n{head_content}\n```\n\n"
                )
                
                file_tokens = self.token_manager.count_tokens(file_output)
                if budget > 0 and (current_tokens + file_tokens > budget):
                    f.write(f"### `{file_path}`\n// File excluded to fit within {budget} token budget.\n\n")
                else:
                    f.write(file_output)
                    current_tokens += file_tokens

        temp_dir_obj.cleanup()
        clipboard_text = None
        if self.config.get('clipboard_mode'):
            try:
                with open(out_filepath, 'r', encoding='utf-8') as cf:
                    clipboard_text = cf.read()
            except Exception as e:
                self.log(f"Warning: Failed to load clipboard text: {e}")

        self.progress(100)
        self.log(f"\nSuccess! PR context file saved to:\n{out_filepath}\nEstimated Total Context Size: ~{current_tokens:,} tokens")
        self.complete(True, {
            "filepath": str(out_filepath),
            "copy_clipboard": self.config.get('clipboard_mode', False),
            "clipboard_text": clipboard_text
        })