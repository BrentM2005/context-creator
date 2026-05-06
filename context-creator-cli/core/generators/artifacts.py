import json
import re
from pathlib import Path

class ArtifactGenerator:
    @staticmethod
    def build_ascii_tree(paths: list[Path]) -> str:
        if not paths: return "No files found."
        tree_dict = {}
        for path in paths:
            current = tree_dict
            for part in path.parts:
                if part not in current: current[part] = {}
                current = current[part]
        def _print_tree(node, prefix=""):
            lines =[]
            keys = sorted(node.keys())
            for i, key in enumerate(keys):
                is_last = (i == len(keys) - 1)
                lines.append(f"{prefix}{'└── ' if is_last else '├── '}{key}")
                if node[key]: lines.extend(_print_tree(node[key], prefix + ("    " if is_last else "│   ")))
            return lines
        return "\n".join(_print_tree(tree_dict))

    @staticmethod
    def build_mermaid_graph(paths: list[Path], root_name: str) -> str:
        if not paths: return "graph TD\n  Empty[No Files]"
        lines =["graph LR", f'  id_root["{root_name}"]']
        node_ids = { "root": "id_root" }
        id_counter = 0
        for path in paths:
            current_str = "root"
            for part in path.parts:
                parent_str = current_str
                current_str = f"{parent_str}/{part}"
                if current_str not in node_ids:
                    id_counter += 1
                    node_id = f"n{id_counter}"
                    node_ids[current_str] = node_id
                    lines.append(f'  {node_id}["{part}"]')
                    lines.append(f'  {node_ids[parent_str]} --> {node_id}')
        return "\n".join(lines)

    @staticmethod
    def parse_deps(file_path: Path, filename: str, deps_dict: dict):
        try:
            if filename == 'package.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    deps = list(data.get('dependencies', {}).keys()) + list(data.get('devDependencies', {}).keys())
                    if deps: deps_dict.setdefault('Node.js (package.json)', set()).update(deps)
            elif filename == 'requirements.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip() and not line.startswith(('#', '-')):
                            pkg = re.split(r'[=><~!]', line.strip())[0].strip()
                            if pkg: deps_dict.setdefault('Python (requirements.txt)', set()).add(pkg)
        except Exception: pass