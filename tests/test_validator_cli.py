import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "blackline_forge_ai" / "validators" / "validator.py"
SINGLE_EXAMPLE = ROOT / "blackline_forge_ai" / "examples" / "single" / "ashline_tactical_hoodie.json"
PACK_EXAMPLE = ROOT / "blackline_forge_ai" / "examples" / "packs" / "ashline_courier_01" / "pack.json"


def run_validator(gate, input_path):
    return subprocess.run(
        ["python3", str(VALIDATOR), "--gate", gate, "--input", str(input_path)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_single_example_passes_generation_gate():
    proc = run_validator("generation", SINGLE_EXAMPLE)
    payload = json.loads(proc.stdout)
    assert proc.returncode == 0
    assert payload["passed"] is True


def test_pack_example_passes_import_gate():
    proc = run_validator("import", PACK_EXAMPLE)
    payload = json.loads(proc.stdout)
    assert proc.returncode == 0
    assert payload["passed"] is True


def test_invalid_gate_fails_with_bfa_000():
    proc = run_validator("finall", SINGLE_EXAMPLE)
    payload = json.loads(proc.stdout)
    assert proc.returncode == 1
    assert payload["violations"][0]["rule"] == "BFA-000"


def test_missing_pack_field_fails_with_bfa_001():
    bad_pack = {
        "schema_version": "1.1.0",
        "pack_id": "pack_01",
        "mode": "pack",
        "theme": {},
        "style_spine": {},
        "palette": {},
        "composition": {},
        "items": [1],
        "fivem": {},
    }

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
        json.dump(bad_pack, tf)
        temp_path = Path(tf.name)

    try:
        proc = run_validator("import", temp_path)
        payload = json.loads(proc.stdout)
    finally:
        temp_path.unlink(missing_ok=True)

    assert proc.returncode == 1
    assert payload["violations"][0]["rule"] == "BFA-001"
    assert "pack_name" in payload["violations"][0]["missing"]
