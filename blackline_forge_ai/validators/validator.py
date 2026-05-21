#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

REQUIRED = ["id","item_name","item_type","category","gender_fit","description","style_axes","color_palette","material","wear_level","fivem","image_prompt"]

def validate_item(obj):
    """
    Identify required fields that are missing or empty in the provided item object.
    
    Parameters:
        obj (dict): The item object to validate.
    
    Returns:
        missing (list[str]): List of required field names that are either absent from `obj` or whose value is `None`, an empty string, or an empty list.
    """
    missing = [k for k in REQUIRED if k not in obj or obj[k] in (None, "", [])]
    return missing

def main():
    """
    Parse command-line arguments, validate the input JSON for required fields when in single-item mode, and print a JSON validation report.
    
    Expects two arguments:
      --gate: identifier string echoed into the report.
      --input: path to a JSON file containing the data object.
    
    Behavior:
      - Loads the JSON object from the file specified by --input.
      - If the object's "mode" is "single", checks required fields and, if any are missing or empty, appends a violation with rule "BFA-001" and a `missing` list of field names.
      - Prints a JSON object with keys:
        - "gate": the provided gate value,
        - "passed": `true` when no violations were found, otherwise `false`,
        - "violations": an array of violation records.
    """
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
