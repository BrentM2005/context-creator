import re
from pathlib import Path
from core.constants import SECRET_PATTERNS, ENTRYPOINT_NAMES

class FileProcessor:
    def __init__(self, config):
        self.config = config

    def redact_secrets(self, content: str):
        total_redacted = 0
        def repl(m):
            nonlocal total_redacted
            total_redacted += 1
            if m.groups() and m.group(1):
                return m.group(0).replace(m.group(1), '***REDACTED***')
            return '***REDACTED***'
        for pattern in SECRET_PATTERNS:
            content, count = pattern.subn(repl, content)
        return content, total_redacted

    def remove_comments(self, content: str, ext: str) -> str:
        try:
            if ext in ['.py', '.rb', '.sh', '.yml', '.yaml']:
                return re.sub(r'(?m)^\s*#.*$', '', content)
            elif ext in['.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.cs', '.go', '.rs', '.php', '.swift', '.kt', '.dart']:
                content = re.sub(r'/\*[\s\S]*?\*/', lambda m: '\n' * m.group(0).count('\n'), content)
                return re.sub(r'(?m)^\s*//.*$', '', content)
            elif ext in['.html', '.xml', '.svg', '.vue', '.svelte']:
                return re.sub(r'<!--[\s\S]*?-->', lambda m: '\n' * m.group(0).count('\n'), content)
            elif ext in['.css', '.scss', '.less']:
                return re.sub(r'/\*[\s\S]*?\*/', lambda m: '\n' * m.group(0).count('\n'), content)
        except Exception:
            pass
        return content

    def apply_formatting(self, content: str, ext: str) -> str:
        if self.config.get('remove_comments'):
            content = self.remove_comments(content, ext)
        lines = content.splitlines()
        if self.config.get('include_line_numbers'):
            formatted_lines =[(f"{i+1:4} | {line}", line) for i, line in enumerate(lines)]
        else:
            formatted_lines =[(line, line) for line in lines]
        if self.config.get('remove_empty_lines'):
            formatted_lines = [fl for fl in formatted_lines if fl[1].strip()]
        return "\n".join([fl[0] for fl in formatted_lines])

    def generate_summary(self, path: Path, content: str) -> str:
        ext = path.suffix.lower()
        classes, functions, imports = [], [],[]
        for line in content.splitlines():
            line = line.strip()
            if ext in ['.py']:
                if line.startswith('class '): classes.append(line[6:].split('(')[0].strip(':'))
                elif line.startswith('def '): functions.append(line[4:].split('(')[0].strip(':'))
                elif line.startswith('import ') or line.startswith('from '): imports.append(line)
            elif ext in['.js', '.ts', '.jsx', '.tsx']:
                if line.startswith('class '): classes.append(line[6:].split('{')[0].strip())
                elif line.startswith('function '): functions.append(line[9:].split('(')[0].strip())
                elif line.startswith('const ') and '=>' in line: 
                    match = re.search(r'const\s+(\w+)\s*=', line)
                    if match: functions.append(match.group(1))
                elif line.startswith('import '): imports.append(line)
        summary =[]
        if classes: summary.append(f"Classes: {', '.join(classes[:5])}" + ("..." if len(classes)>5 else ""))
        if functions: summary.append(f"Functions: {', '.join(functions[:10])}" + ("..." if len(functions)>10 else ""))
        if imports: summary.append(f"Key Imports: {len(imports)} found")
        if summary: return "\n".join([f"> {s}" for s in summary]) + "\n\n"
        return ""

    def calculate_score(self, path: Path, root_path: Path) -> int:
        score = 0
        name = path.name.lower()
        rel_parts = path.relative_to(root_path).parts
        if name in ENTRYPOINT_NAMES: score += 50
        if any(part in['src', 'core', 'lib', 'app'] for part in rel_parts): score += 20
        if name in['readme.md', 'package.json', 'requirements.txt', 'dockerfile', 'docker-compose.yml']: score += 30
        if any(part in ['test', 'tests', 'spec', 'mocks'] for part in rel_parts): score -= 20
        score -= (len(rel_parts) * 2) 
        return score

    def is_binary_file(self, filepath: Path) -> bool:
        try:
            with open(filepath, 'rb') as f:
                if b'\0' in f.read(1024): return True
            with open(filepath, 'r', encoding='utf-8') as f: f.read(1024)
            return False
        except (UnicodeDecodeError, PermissionError): return True