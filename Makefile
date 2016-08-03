# Project configuration
PROJECT_NAME = awsudo
MODULE = $(PROJECT_NAME).py

# Call these functions before/after each target to maintain a coherent display
START_TARGET = @printf "[$(shell date +"%H:%M:%S")] %-40s" "$(1)"
END_TARGET = @printf "\033[32;1mOK\033[0m\n"

# Parameter expansion
PYTEST_OPTS ?=


.PHONY: clean help \
	check_pep8 check_pep257 check_pylint check_xenon \
	check_lint check_test \
	check_test_report check check_ci \


help:
	@echo "check_pep8         Apply pep8 checks (core coding style)"
	@echo "check_pep257       Apply pep257 checks (docstring style)"
	@echo "check_pylint       Apply pylint checks (code quality)"
	@echo "check_xenon        Apply xenon checks (code complexity)"
	@echo "check_lint         Apply pep8, pep257, pylint, xenon"
	@echo "check_test         Apply py.test"
	@echo "check_test_report  Apply py.test and generate full reports"
	@echo "check              Apply check_lint, check_test"
	@echo "check_ci           Apply clean, check_lint, check_test_report"
	@echo "clean              Remove useless temporary files"


check_pep8:
	$(call START_TARGET,Checking pep8)
	@pep8 $(MODULE)
	$(call END_TARGET)


check_pep257:
	$(call START_TARGET,Checking pep257)
	@pep257 $(MODULE)
	$(call END_TARGET)


check_pylint:
	$(call START_TARGET,Checking pylint)
	@pylint -rno $(MODULE)
	$(call END_TARGET)


check_xenon:
	$(call START_TARGET,Checking xenon)
	@xenon -m A -a A -b A --no-assert $(MODULE)
	$(call END_TARGET)


check_test:
	$(call START_TARGET,Checking tests)
	@py.test -q -x $(PYTEST_OPTS)


check_test_report:
	$(call START_TARGET,Checking tests)
	@echo
	@py.test -vv --cov --cov-report=term-missing --cov-report=html \
		--cov-report=xml --junit-xml=junit.xml

check_lint: check_pep8 check_pep257 check_pylint check_xenon


check: check_lint check_test


check_ci: clean check_lint check_test_report


clean:
	$(call START_TARGET,Cleaning)
	@find . -type f -name '*.pyc' -exec rm {} \;
	@rm -rf dist/* *.egg-info .cache .eggs
	@rm -rf htmlcov .coverage
	@rm -f junit.xml
	$(call END_TARGET)
