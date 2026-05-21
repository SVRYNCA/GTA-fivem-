PYTHON=python3

.PHONY: build check validate

build:
	$(PYTHON) -m build

check:
	$(PYTHON) -m pip install --upgrade build wheel setuptools
	$(PYTHON) -m build

validate:
	$(PYTHON) -m blackline_forge_ai.validators.validator --gate generation --input blackline_forge_ai/examples/single/ashline_tactical_hoodie.json
	$(PYTHON) -m blackline_forge_ai.validators.validator --gate import --input blackline_forge_ai/examples/packs/ashline_courier_01/pack.json
