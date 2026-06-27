PYTHON ?= python

.PHONY: install check validate clean-outputs

install:
	$(PYTHON) -m pip install -r requirements.txt

check:
	$(PYTHON) -m compileall -q src/evaluate src/simulator/*.py examples scripts/validate_dataset.py
	$(PYTHON) scripts/validate_dataset.py
	PYTHONPATH=src $(PYTHON) -m evaluate.batch --help >/dev/null

validate:
	$(PYTHON) scripts/validate_dataset.py

clean-outputs:
	rm -rf @output
