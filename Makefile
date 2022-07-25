## =====================================================================================
##  C O P Y R I G H T
## -------------------------------------------------------------------------------------
##  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
##
##  Author(s):
##  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
## =====================================================================================

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINX_OPTS     =
BUILD_DIR       = .build
DOCS_SOURCE_DIR = .

.PHONY: help clean html doxygen doxysphinx sphinx

help:
	@echo "Please use make <target> where <target> is one of"
	@echo "  sphinx      to run sphinx."
	@echo "  doxygen     to run doxygen."
	@echo "  doxysphinx  to run doxysphinx."
	@echo "  html        to run everything in correct order to generate the documentation."
	@echo "  clean       to clean up everything"

clean:
	@poetry run doxysphinx --verbosity=DEBUG clean $(DOCS_SOURCE_DIR) $(BUILD_DIR)/html demo/demo.doxyfile
# cannot use rm here because it's not portable (win/linux)
	@poetry run python -c 'exec("import shutil\nimport glob\n\nfor result in glob.glob(\"docs/doxygen/demo/*\"): shutil.rmtree(result)")'
	@poetry run python -c 'exec("import shutil\nimport glob\n\nfor result in glob.glob(\".build/*\"): shutil.rmtree(result)")'

doxygen:
	@doxygen demo/demo.doxyfile

doxysphinx:
	@poetry run doxysphinx --verbosity=DEBUG build $(DOCS_SOURCE_DIR) $(BUILD_DIR)/html demo/demo.doxyfile

doxysphinx_with_dir:
	@poetry run doxysphinx --verbosity=DEBUG build $(DOCS_SOURCE_DIR) $(BUILD_DIR)/html docs/doxygen/demo/html

sphinx:
	@poetry run sphinx-build -M html "$(DOCS_SOURCE_DIR)" "$(BUILD_DIR)" '--keep-going' '-j' 'auto' $(SPHINX_OPTS)

profile: clean doxygen
	@poetry run python -m cProfile -o .doxysphinx.prof doxysphinx/cli.py --verbosity=DEBUG build $(DOCS_SOURCE_DIR) $(BUILD_DIR) demo/demo.doxyfile
	@poetry run snakeviz .doxysphinx.prof
	@rm .doxysphinx.prof

html: doxygen doxysphinx sphinx
	@echo ""
	@echo "Build finished. The Documentation is in $(BUILD_DIR)/html."
