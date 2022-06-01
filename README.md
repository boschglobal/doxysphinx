<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
=====================================================================================
-->

<div align="center">

<img src="docs/resources/doxysphinx_logo.svg" alt="doxysphinx" width=500 />

</div>

---

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE.md)
[![Pypi package](https://img.shields.io/pypi/v/doxysphinx?style=plastic)](https://pypi.org/project/doxysphinx/)
[![supported Python versions](https://img.shields.io/pypi/pyversions/doxysphinx)](https://pypi.org/project/doxysphinx/)
[![Build action: CI](https://github.com/boschglobal/doxysphinx/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/boschglobal/doxysphinx/actions/workflows/ci.yml)
[![Build action: CD](https://github.com/boschglobal/doxysphinx/actions/workflows/cd.yml/badge.svg?tag=latest)](https://github.com/boschglobal/doxysphinx/actions/workflows/cd.yml)

Doxysphinx is a [Doxygen](https://doxygen.nl) and [Sphinx](https://sphinx-doc.org) integration tool.

It will make the doxygen documentation appear inside the sphinx documentation frame.

It comes as an easy-to-use cli tool and typically runs right after doxygen created it's html documentation.
Doxysphinx creates restructured text (.rst) files out of these (doxygen) html files.

Afterwards sphinx will pick up these rst files and create an integrated documentation
(theming is applied, search etc.).

## Links

📚 [Doxysphinx Overview](https://boschglobal.github.io/doxysphinx)

🚀 [Getting Started](https://boschglobal.github.io/doxysphinx/docs/getting_started.html)

💻 [Developer Quickstart](https://boschglobal.github.io/doxysphinx/docs/dev_guide.html)

🤖 [Releases](https://github.com/boschglobal/doxysphinx/releases)
