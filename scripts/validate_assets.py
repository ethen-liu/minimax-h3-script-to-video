from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a script-to-video asset manifest.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    root = args.manifest.parent.parent
    errors: list[str] = []
    characters = data.get("characters", [])
    scenes = data.get("scenes", [])
    props = data.get("props", [])
    if not characters:
        errors.append("manifest has no characters")
    if not scenes:
        errors.append("manifest has no scenes")
    seen_ids: set[str] = set()
    for kind, entries in (("character", characters), ("scene", scenes), ("prop", props)):
        for entry in entries:
            item_id = entry.get("id")
            if not item_id:
                errors.append(f"{kind} is missing id")
                continue
            if item_id in seen_ids:
                errors.append(f"duplicate asset id: {item_id}")
            seen_ids.add(item_id)
            path = entry.get("path")
            if not path:
                errors.append(f"{kind} {item_id} is missing path")
            elif not (root / path).exists():
                errors.append(f"{kind} {item_id} path does not exist: {path}")
            if kind == "character":
                if entry.get("sheet_aspect") != "3:4":
                    errors.append(f"character {item_id} must declare sheet_aspect=3:4")
                if not entry.get("audio_path"):
                    errors.append(f"character {item_id} is missing audio_path")
                required = {"top_left_close_front", "top_right_close_half_side", "bottom_left_full_front_no_face", "bottom_right_full_back_no_face"}
                if set(entry.get("panels", [])) != required:
                    errors.append(f"character {item_id} must declare the four required panels")
    for entry in data.get("optional_assets", []):
        if entry.get("status") not in {"planned", "provided", "generated", "approved", "not_needed"}:
            errors.append(f"optional asset has invalid status: {entry.get('id', '<unknown>')}")
    if errors:
        print("ASSET MANIFEST INVALID")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(json.dumps({"valid": True, "characters": len(characters), "scenes": len(scenes), "props": len(props)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
