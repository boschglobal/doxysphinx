<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
 - Nirmal Sasidharan, Robert Bosch Gmbh
 - Wolfgang Ulmer, Robert Bosch GmbH
=====================================================================================
-->

<div align="center">

<img src="https://raw.githubusercontent.com/boschglobal/doxysphinx/main/docs/resources/doxysphinx_logo.svg" alt="doxysphinx" width=500 />

</div>

---

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE.md)
[![Pypi package](https://img.shields.io/pypi/v/doxysphinx)](https://pypi.org/project/doxysphinx/)
[![supported Python versions](https://img.shields.io/pypi/pyversions/doxysphinx)](https://pypi.org/project/doxysphinx/)
[![Build action: CI](https://github.com/boschglobal/doxysphinx/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/boschglobal/doxysphinx/actions/workflows/ci.yml)
[![Build action: CD](https://github.com/boschglobal/doxysphinx/actions/workflows/cd.yml/badge.svg?tag=latest)](https://github.com/boschglobal/doxysphinx/actions/workflows/cd.yml)

Doxysphinx is a [Doxygen](https://doxygen.nl) and [Sphinx](https://sphinx-doc.org) integration tool.

It is an easy-to-use cli tool and typically runs right after Doxygen generation.
It reuses the Doxygen generated HTML output and integrates it into Sphinx document generation.
With this, Doxysphinx supports all known Doxygen features and at the same time integrates well with the Sphinx output (for example, Sphinx-Themes, search etc.).
Doxysphinx, also supports [restructured text (rST) annotations](https://github.com/boschglobal/doxysphinx/blob/main/docs/using_rst_in_doxygen.md) within C++ files.

Internally, Doxysphinx creates an rST file for each (Doxygen) HTML file and includes the HTML using `.. raw:: html` directive.
Later Sphinx picks up these rST files and creates an integrated documentation.

Check out Doxysphinx alternatives [here](https://github.com/boschglobal/doxysphinx/blob/main/docs/alternatives.md).

## Links

📚 [Doxysphinx Overview](https://boschglobal.github.io/doxysphinx)

🚀 [Getting Started](https://boschglobal.github.io/doxysphinx/docs/getting_started.html)

💻 [Developer Quickstart](https://boschglobal.github.io/doxysphinx/docs/dev_guide.html)

🤖 [Releases](https://github.com/boschglobal/doxysphinx/releases)
