#!/usr/bin/env python3
import argparse
import sys
import threading
import signal
from core.generator import ContextGenerator
from core.constants import DOC_TEMPLATES

# --- ANSI Color Definitions ---
class Colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

BANNER = f"""{Colors.PURPLE}{Colors.BOLD}
   ______            __            __   ______                 __           
  / ____/___  ____  / /____  _  __/ /_ / ____/_________  ____ _/ /_____  _____
 / /   / __ \\/ __ \\/ __/ _ \\| |/_/ __// /   / ___/ _ \\/ __ `/ __/ __ \\/ ___/
/ /___/ /_/ / / / / /_/  __/>  </ /_ / /___/ /  /  __/ /_/ / /_/ /_/ / /    
\\____/\\____/_/ /_/\\__/\\___/_/|_|\\__/ \\____/_/   \\___/\\__,_/\\__/\\____/_/     
{Colors.CYAN}                                                   Terminal Edition{Colors.END}
"""

class ColorfulParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        print(BANNER)
        super().print_help(file)

    def error(self, message):
        print(BANNER)
        print(f"{Colors.RED}{Colors.BOLD}[!] Error: {message}{Colors.END}\n")
        self.print_help()
        sys.exit(2)

def colorize_log(msg):
    """Adds a splash of color to console logs based on keywords."""
    if "Phase" in msg:
        return f"{Colors.CYAN}{Colors.BOLD}{msg}{Colors.END}"
    elif "Warning" in msg:
        return f"{Colors.YELLOW}{msg}{Colors.END}"
    elif "CRITICAL" in msg or "Error" in msg:
        return f"{Colors.RED}{Colors.BOLD}{msg}{Colors.END}"
    elif "Success" in msg:
        return f"{Colors.GREEN}{Colors.BOLD}{msg}{Colors.END}"
    elif "Cancelled" in msg:
        return f"{Colors.YELLOW}{msg}{Colors.END}"
    return f"{Colors.BLUE}{msg}{Colors.END}"

def main():
    parser = ColorfulParser(
        description=f"{Colors.BOLD}Context Creator CLI{Colors.END} - Effortlessly generate LLM context packages from codebases.",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False 
    )

    cmd_group = parser.add_argument_group(f"{Colors.PURPLE}{Colors.BOLD}Core Commands{Colors.END}")
    cmd_group.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    cmd_group.add_argument('mode', nargs='?', choices=['local', 'remote', 'pr'], 
                        help="Source type (local, remote, pr). Omit if using template flags.")
    cmd_group.add_argument('input', nargs='?', default="", 
                        help="Input directory path, Repo URL, or PR/MR URL")
    
    tpl_group = parser.add_argument_group(f"{Colors.YELLOW}{Colors.BOLD}Templates{Colors.END}")
    tpl_group.add_argument('--list-templates', action='store_true', help="List available prompt templates and exit")
    tpl_group.add_argument('--get-template', type=str, metavar="NAME", help="Output a specific prompt template and exit")

    src_group = parser.add_argument_group(f"{Colors.CYAN}{Colors.BOLD}Source & Output Options{Colors.END}")
    src_group.add_argument('--pat', default="", help="Personal Access Token for private Repos / PRs")
    src_group.add_argument('--out-dir', default=".", help="Output directory (default: current directory)")
    src_group.add_argument('--out-file', default="my_project.md", help="Output file name (default: my_project.md)")
    src_group.add_argument('--format', dest='llm_opt',
                        choices=[
                            "ChatGPT / Standard (Markdown)", 
                            "Claude Optimized (XML)",
                            "Gemini Optimized (Delimited)", 
                            "JSON Structured Export", 
                            "Raw Text"
                        ],
                        default="ChatGPT / Standard (Markdown)", help="Output format for specific LLMs")
    src_group.add_argument('--no-tech-stack', action='store_false', dest='tech_stack', help="Disable Tech Stack artifact")
    src_group.add_argument('--mermaid', action='store_true', help="Generate Mermaid Graph artifact")
    src_group.add_argument('--prompt-pack', action='store_true', help="Generate Prompt Pack artifact")
    src_group.add_argument('--clipboard', action='store_true', help="Copy output context to clipboard (requires pyperclip)")

    flt_group = parser.add_argument_group(f"{Colors.GREEN}{Colors.BOLD}Filters & Limits{Colors.END}")
    flt_group.add_argument('--max-size', type=int, default=500, help="Max file size in KB (default: 500)")
    flt_group.add_argument('--max-lines', type=int, default=2000, help="Max lines per file (default: 2000)")
    flt_group.add_argument('--no-gitignore', action='store_false', dest='use_gitignore', help="Do not respect .gitignore rules")
    flt_group.add_argument('--line-numbers', action='store_true', dest='include_line_numbers', help="Include line numbers in code")
    flt_group.add_argument('--remove-comments', action='store_true', help="Remove code comments to save tokens")
    flt_group.add_argument('--remove-empty', action='store_true', dest='remove_empty_lines', help="Remove empty lines")
    flt_group.add_argument('--extensions', default="", help="Comma-separated specific extensions to include (e.g., .py,.js)")
    flt_group.add_argument('--ignores', default="", dest='custom_ignores', help="Comma-separated custom directories to ignore")

    ai_group = parser.add_argument_group(f"{Colors.BLUE}{Colors.BOLD}AI Optimization{Colors.END}")
    ai_group.add_argument('--git-mode', choices=["All Files", "Changed vs HEAD", "Changed vs main"], 
                        default="All Files", help="Git sync mode (default: All Files)")
    ai_group.add_argument('--budget', default="None", 
                        help="Token budget: 'GPT-4o (128k)', 'Claude (200k)', 'Gemini (1M)', or a custom number")
    ai_group.add_argument('--no-secrets', action='store_false', dest='secret_scan', help="Disable auto-redacting secrets")
    ai_group.add_argument('--no-summaries', action='store_false', dest='summaries', help="Disable generating code summaries")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.list_templates:
        print(BANNER)
        print(f"{Colors.YELLOW}{Colors.BOLD}Available Documentation Templates:{Colors.END}")
        for tpl in DOC_TEMPLATES.keys():
            print(f"  {Colors.GREEN}✓{Colors.END} {tpl}")
        sys.exit(0)
    
    if args.get_template:
        template = DOC_TEMPLATES.get(args.get_template)
        if template:
            print(BANNER)
            print(f"{Colors.YELLOW}--- Template: {args.get_template} ---{Colors.END}\n")
            print(template)
            print(f"\n{Colors.YELLOW}-----------------------------------{Colors.END}\n")
            sys.exit(0)
        else:
            parser.error(f"Template '{args.get_template}' not found. Use --list-templates to see available options.")

    if not args.mode or not args.input:
        parser.error("You must specify a 'mode' (local, remote, pr) and an 'input' (path or URL).")

    custom_budget = "0"
    token_budget_str = args.budget
    if token_budget_str.isdigit():
        custom_budget = token_budget_str
        token_budget_str = "Custom"

    config = {
        "mode": args.mode,
        "input_dir": args.input if args.mode == 'local' else "",
        "repo_url": args.input if args.mode == 'remote' else "",
        "pr_url": args.input if args.mode == 'pr' else "",
        "pat": args.pat,
        "output_dir": args.out_dir,
        "output_file": args.out_file,
        "llm_opt": args.llm_opt,
        "generate_tech_stack": args.tech_stack,
        "mermaid_graph": args.mermaid,
        "prompt_packs": args.prompt_pack,
        "clipboard_mode": args.clipboard,
        "max_size_kb": str(args.max_size),
        "max_lines": str(args.max_lines),
        "use_gitignore": args.use_gitignore,
        "include_line_numbers": args.include_line_numbers,
        "remove_comments": args.remove_comments,
        "remove_empty_lines": args.remove_empty_lines,
        "extensions": args.extensions,
        "custom_ignores": args.custom_ignores,
        "git_mode": args.git_mode,
        "token_budget": token_budget_str,
        "custom_budget": custom_budget,
        "secret_scan": args.secret_scan,
        "summaries": args.summaries,
    }

    cancel_event = threading.Event()

    def log_cb(msg):
        if msg.strip():
            colored_msg = colorize_log(msg)
            sys.stdout.write(f"\033[K{colored_msg}\n")
            sys.stdout.flush()

    def progress_cb(val):
        bar_length = 40
        filled = int(bar_length * (val / 100))
        bar = '█' * filled + '░' * (bar_length - filled)
        sys.stdout.write(f"\r\033[K{Colors.PURPLE}Progress: [{bar}]{Colors.END} {Colors.BOLD}{val:.1f}%{Colors.END}")
        sys.stdout.flush()
        if val >= 100:
            print() 

    def complete_cb(success, payload):
        if success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}[✓] Operation completed successfully!{Colors.END}")
            if payload and payload.get("copy_clipboard") and payload.get("clipboard_text"):
                try:
                    import pyperclip
                    pyperclip.copy(payload["clipboard_text"])
                    print(f"{Colors.GREEN}[✓] Output automatically copied to clipboard.{Colors.END}")
                except ImportError:
                    print(f"\n{Colors.YELLOW}[!] Could not copy to clipboard: 'pyperclip' is not installed.{Colors.END}")
                    print(f"    Run: {Colors.CYAN}pip install pyperclip{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}[x] Operation failed or was cancelled.{Colors.END}")
            if payload and isinstance(payload, dict) and payload.get("error"):
                print(f"{Colors.RED}Error detail: {payload['error']}{Colors.END}")
        sys.exit(0 if success else 1)

    def signal_handler(sig, frame):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[!] Cancelling operation... cleaning up.{Colors.END}")
        cancel_event.set()

    signal.signal(signal.SIGINT, signal_handler)

    print(BANNER)
    print(f"{Colors.BOLD}Starting Context Generator ({Colors.CYAN}{args.mode}{Colors.END}{Colors.BOLD} mode)...{Colors.END}\n")
    
    generator = ContextGenerator(config, cancel_event, log_cb, progress_cb, complete_cb)
    
    try:
        generator.run()
    except Exception as e:
        print(f"\n{Colors.RED}{Colors.BOLD}[!] Unexpected Crash: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()