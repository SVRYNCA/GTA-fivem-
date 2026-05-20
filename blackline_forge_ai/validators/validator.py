#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

REQUIRED = ["id","item_name","item_type","category","gender_fit","description","style_axes","color_palette","material","wear_level","fivem","image_prompt"]

def validate_item(obj):
    missing = [k for k in REQUIRED if k not in obj or obj[k] in (None, "", [])]
    return missing

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gate", required=True)
    p.add_argument("--input", required=True)
    args = p.parse_args()

    data = json.loads(Path(args.input).read_text())
    violations = []

    if data.get("mode") == "single":
        missing = validate_item(data)
        if missing:
            violations.append({"rule":"BFA-001","missing":missing})

    print(json.dumps({"gate": args.gate, "passed": len(violations) == 0, "violations": violations}, indent=2))

if __name__ == "__main__":
    main()
