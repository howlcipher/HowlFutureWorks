.PHONY: validate test render audit dist verify-dist

validate:
	python tools/orgctl.py validate

render:
	python tools/orgctl.py render-all

test:
	python -m pytest -q

audit:
	python tools/orgctl.py validate
	python -m pytest -q
	python -m compileall -q tools tests
	git diff --check

dist:
	python tools/package_release.py build

verify-dist:
	python tools/package_release.py verify
