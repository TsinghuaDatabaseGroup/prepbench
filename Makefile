PYTHON ?= python3

.PHONY: install check check-all validate verify-reference-outputs release-validate clean clean-outputs

install:
	$(PYTHON) -m pip install -r requirements.txt

check:
	$(PYTHON) -m compileall -q src/prepbench src/evaluate src/simulator/*.py examples scripts/validate_dataset.py scripts/verify_reference_outputs.py
	$(PYTHON) scripts/validate_dataset.py
	PYTHONPATH=src $(PYTHON) -m evaluate.batch --help >/dev/null

check-all: check
	$(PYTHON) -m compileall -q reference/solutions
	$(PYTHON) scripts/verify_reference_outputs.py

validate:
	$(PYTHON) scripts/validate_dataset.py

verify-reference-outputs:
	$(PYTHON) scripts/verify_reference_outputs.py

release-validate: check-all

clean: clean-outputs
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
	rm -rf build dist src/prepbench.egg-info .pytest_cache

clean-outputs:
	rm -rf @output @out-info
