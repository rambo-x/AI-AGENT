from pathlib import Path
from typing import Dict, List
from datetime import datetime
import json

IGNORE_DIRS = {
    ".git",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "node_modules",
    "logs",
}

LANGUAGE_MAP = {
    ".py": "python",
    ".json": "json",
    ".js": "javascript",
    ".ts": "typescript",
    ".md": "markdown",
    ".txt": "text",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".env": "env",
}


class ProjectScanner:
    """
    Scanner v1.0

    Bertugas memindai struktur project dan menghasilkan
    project_index.json.

    Modul ini dianggap STABLE.
    """

    def __init__(self, root: str):
        self.root = Path(root).resolve()

    def _language(self, path: Path) -> str:
        return LANGUAGE_MAP.get(path.suffix.lower(), "unknown")

    def _component(self, relative: Path) -> str:
        """
        File di root project dianggap komponen 'root'.
        Folder level pertama menjadi nama komponen.
        """
        if len(relative.parts) == 1:
            return "root"

        return relative.parts[0]

    def scan(self) -> Dict:

        files: List[Dict] = []
        folders = set()

        for path in self.root.rglob("*"):

            relative = path.relative_to(self.root)

            if any(part in IGNORE_DIRS for part in relative.parts):
                continue

            if path.is_dir():
                folders.add(str(relative))
                continue

            stat = path.stat()

            component = self._component(relative)

            files.append({
                "path": str(relative),
                "filename": path.name,
                "component": component,
                "is_root": component == "root",
                "depth": len(relative.parts),
                "language": self._language(path),
                "extension": path.suffix.lower(),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat()
            })

        return {
            "root": str(self.root),
            "generated_at": datetime.now().isoformat(),
            "total_files": len(files),
            "python_files": sum(
                1 for f in files
                if f["language"] == "python"
            ),
            "folders": sorted(folders),
            "files": sorted(
                files,
                key=lambda x: x["path"]
            )
        }

    def save(
        self,
        output="database/project_index.json"
    ) -> str:

        data = self.scan()

        Path(output).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(output, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return output

    @staticmethod
    def load(
        path="database/project_index.json"
    ) -> Dict:

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
