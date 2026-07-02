PYTHON ?= python3

.PHONY: install check validate verify-reference-outputs clean-outputs

install:
	$(PYTHON) -m pip install -r requirements.txt

check:
	$(PYTHON) -m compileall -q src/evaluate src/simulator/*.py examples reference/solutions scripts/validate_dataset.py scripts/verify_reference_outputs.py
	$(PYTHON) scripts/validate_dataset.py
	PYTHONPATH=src $(PYTHON) -m evaluate.batch --help >/dev/null

validate:
	$(PYTHON) scripts/validate_dataset.py

verify-reference-outputs:
	$(PYTHON) scripts/verify_reference_outputs.py

clean-outputs:
	rm -rf @output
