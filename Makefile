## =====================================================================================
##  C O P Y R I G H T
## -------------------------------------------------------------------------------------
##  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
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
	@poetry run python -c 'exec("import shutil\nimport glob\n\nfor result in glob.glob(\"docs/doxygen/graphviz/*\"): shutil.rmtree(result)")'
	@poetry run python -c 'exec("import shutil\nimport glob\n\nfor result in glob.glob(\".build/*\"): shutil.rmtree(result)")'


# targets for demo project
doxygen_demo:
	@doxygen demo/demo.doxyfile

doxysphinx_demo:
	@poetry run doxysphinx --verbosity=DEBUG build $(DOCS_SOURCE_DIR) $(BUILD_DIR)/html demo/demo.doxyfile

doxysphinx_demo_with_dir:
	@poetry run doxysphinx --verbosity=DEBUG build $(DOCS_SOURCE_DIR) $(BUILD_DIR)/html docs/doxygen/demo/html

# targets for graphviz project
# -> ATTENTION: Before you can use them you have to download graphviz (see ./demo/load_additional_demos.sh)
doxygen_graphviz:
	@cd demo/graphviz; doxygen Doxyfile.in

doxysphinx_graphviz:
	@mkdir -p docs/doxygen/graphviz
	@cp -R demo/graphviz/doxygen/html docs/doxygen/graphviz
	@poetry run doxysphinx --verbosity=DEBUG build $(DOCS_SOURCE_DIR) $(BUILD_DIR)/html docs/doxygen/graphviz/html

# sphinx
sphinx:
	@poetry run sphinx-build -M html "$(DOCS_SOURCE_DIR)" "$(BUILD_DIR)" '--keep-going' '-j' 'auto' $(SPHINX_OPTS)

# for profiling...
profile: clean doxygen_demo
	@poetry run python -m cProfile -o .doxysphinx.prof doxysphinx/cli.py --verbosity=DEBUG build $(DOCS_SOURCE_DIR) $(BUILD_DIR) demo/demo.doxyfile
	@poetry run snakeviz .doxysphinx.prof
	@rm .doxysphinx.prof

# some aliases
doxygen: doxygen_demo

doxysphinx: doxysphinx_demo

html: doxygen doxysphinx sphinx
	@echo ""
	@echo "Build finished. The Documentation is in $(BUILD_DIR)/html."
