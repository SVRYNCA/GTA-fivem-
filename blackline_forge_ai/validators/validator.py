#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SCHEMA_REQUIRED = {
    "single": ["schema_version", "id", "mode", "item_name", "item_type", "category", "gender_fit", "description", "style_axes", "color_palette", "material", "wear_level", "fivem", "image_prompt"],
    "pack": ["schema_version", "pack_id", "pack_name", "mode", "theme", "style_spine", "palette", "composition", "items", "fivem"],
    "character": ["schema_version", "character_id", "mode", "persona", "equipped_items"],
}


def missing_fields(obj, required):
    return [k for k in required if k not in obj or obj[k] in (None, "", [])]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gate", required=True)
    p.add_argument("--input", required=True)
    args = p.parse_args()

    data = json.loads(Path(args.input).read_text())
    violations = []

    mode = data.get("mode")
    required = SCHEMA_REQUIRED.get(mode)

    if required is None:
        violations.append({
            "rule": "BFA-000",
            "error": f"unsupported mode '{mode}'",
            "allowed_modes": sorted(SCHEMA_REQUIRED.keys()),
        })
    else:
        missing = missing_fields(data, required)
        if missing:
            violations.append({"rule": "BFA-001", "mode": mode, "missing": missing})

    print(json.dumps({"gate": args.gate, "passed": len(violations) == 0, "violations": violations}, indent=2))


if __name__ == "__main__":
    main()
