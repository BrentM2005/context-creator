import subprocess
import fnmatch
from pathlib import Path

class GitManager:
    def __init__(self, log_cb):
        self.log = log_cb

    def get_changed_files(self, repo_path: Path, mode: str) -> set:
        try:
            cmd =["git", "-C", str(repo_path), "diff", "--name-only"]
            if mode == "Changed vs main":
                cmd.append("main")
            elif mode == "Changed vs HEAD":
                cmd.append("HEAD")
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0 and mode == "Changed vs main":
                cmd[-1] = "master"
                res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                changed = set(res.stdout.splitlines())
                untracked_cmd =["git", "-C", str(repo_path), "ls-files", "--others", "--exclude-standard"]
                untracked_res = subprocess.run(untracked_cmd, capture_output=True, text=True)
                if untracked_res.returncode == 0:
                    changed.update(untracked_res.stdout.splitlines())
                return {(repo_path / f).resolve() for f in changed if f.strip()}
            else:
                self.log(f"Warning: Git diff failed ({res.stderr.strip()})")
                return None
        except Exception as e:
            self.log(f"Git command error: {e}")
            return None

    def parse_gitignore(self, root_path: Path):
        patterns =[]
        try:
            with open(root_path / '.gitignore', 'r', encoding='utf-8') as f:
                patterns =[line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception: pass
        return patterns

    def is_ignored_by_gitignore(self, path: Path, root_path: Path, patterns: list) -> bool:
        if not patterns: return False
        try:
            rel_path = path.relative_to(root_path).as_posix()
            parts = rel_path.split('/')
            for pat in (p.strip('/') for p in patterns):
                if pat in parts or fnmatch.fnmatch(rel_path, pat) or fnmatch.fnmatch(rel_path, f"*/{pat}") or fnmatch.fnmatch(rel_path, f"{pat}/*"):
                    return True
        except ValueError: pass
        return False