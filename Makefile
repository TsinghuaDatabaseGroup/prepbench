PYTHON ?= python

.PHONY: install lint run clean-outputs

install:
	$(PYTHON) -m pip install -r requirements.txt

lint:
	$(PYTHON) -m compileall src run.py methods/prepagent/run_prepagent.py

# Usage: make run CASE=1 RUN_MODE=orig MODEL=openai/gpt-5.2
run:
	$(PYTHON) run.py --case $(CASE) $(if $(MODE),--mode $(MODE),) $(if $(MODEL),--model $(MODEL),) $(if $(RUN_MODE),--run_mode $(RUN_MODE),)

clean-outputs:
	rm -rf @output data_synthesis/output
