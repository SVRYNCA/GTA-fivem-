# Blackline Forge AI

Production-oriented specification bundle for generating FiveM/GTA roleplay fashion assets.

## Included
- JSON Schemas for isolated items, packs, and character-mode outputs.
- Validator ruleset and Python reference validator.
- Prompt pack for generator modes.
- Registry assets (palettes, materials, blocklists, slot reference).
- Pipeline state machine and examples.

## Quick start
```bash
python3 blackline_forge_ai/validators/validator.py --gate generation --input blackline_forge_ai/examples/single/ashline_tactical_hoodie.json
python3 blackline_forge_ai/validators/validator.py --gate import --input blackline_forge_ai/examples/packs/ashline_courier_01/pack.json
```
