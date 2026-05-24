#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ALLOWED_GATES = {"generation", "import", "publish"}
SCHEMA_REQUIRED = {
    "single": [
        "schema_version",
        "id",
        "mode",
        "item_name",
        "item_type",
        "category",
        "gender_fit",
        "description",
        "style_axes",
        "color_palette",
        "material",
        "wear_level",
        "fivem",
        "image_prompt",
    ],
    "pack": [
        "schema_version",
        "pack_id",
        "pack_name",
        "mode",
        "theme",
        "style_spine",
        "palette",
        "composition",
        "items",
        "fivem",
    ],
    "character": [
        "schema_version",
        "character_id",
        "mode",
        "persona",
        "equipped_items",
    ],
}


def missing_fields(obj, required):
    return [k for k in required if k not in obj or obj[k] in (None, "", [])]


def report_and_exit(gate, violations):
    passed = len(violations) == 0
    print(json.dumps({"gate": gate, "passed": passed, "violations": violations}, indent=2))
    sys.exit(0 if passed else 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    violations = []
    if args.gate not in ALLOWED_GATES:
        violations.append(
            {
                "rule": "BFA-000",
                "error": f"unsupported gate '{args.gate}'",
                "allowed_gates": sorted(ALLOWED_GATES),
            }
        )
        report_and_exit(args.gate, violations)

    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        violations.append({"rule": "BFA-000", "error": f"invalid input: {err}"})
        report_and_exit(args.gate, violations)

    mode = data.get("mode")
    required = SCHEMA_REQUIRED.get(mode)

    if required is None:
        violations.append(
            {
                "rule": "BFA-000",
                "error": f"unsupported mode '{mode}'",
                "allowed_modes": sorted(SCHEMA_REQUIRED.keys()),
            }
        )
    else:
        missing = missing_fields(data, required)
        if missing:
            violations.append({"rule": "BFA-001", "mode": mode, "missing": missing})

    report_and_exit(args.gate, violations)


if __name__ == "__main__":
    main()
