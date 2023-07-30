.DEFAULT_GOAL := minify

PYTHON := $(shell command -v python3 >/dev/null 2>&1 && echo python3 || echo python)

minify:     # minify html+js (default)
	npm run build

install:    # install npm dependencies for minification
	npm install

clean:      # remove generated files
	rm -f -v mediabro.min.html js/main.min.js

run:
	$(PYTHON) mediabrowser.py --browser

help:       # show available targets
	@grep '^[[:alnum:]]\+:' Makefile