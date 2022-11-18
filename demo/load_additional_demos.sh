#!/usr/bin/env bash

# This script will load additional oss demo projects.

# graphviz
git clone --depth 1 https://gitlab.com/graphviz/graphviz.git
rm -rf graphviz/.git # get rid of git repo...
echo "" >> graphviz/Doxyfile.in
echo "HTML_EXTRA_STYLESHEET = ../../external/doxygen-awesome-css/doxygen-awesome.css" >> graphviz/Doxyfile.in

# for future use
#git clone --depth 1 https://github.com/vrogier/ocilib.git
#rm -rf ocilib/.git # get rid of git repo...
