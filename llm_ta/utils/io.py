import json
from pathlib import Path
from typing import Any, Union

def load_json(path: Path) -> Any:
    """Load JSON file."""
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(data: list | dict, path: Path) -> None:
    """Save data to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
