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
[![Build action: CD](https://github.com/boschglobal/doxysphinx/actions/workflows/cd.yml/badge.svg?branch=main)](https://github.com/boschglobal/doxysphinx/actions/workflows/cd.yml)

Doxysphinx is a [Doxygen](https://doxygen.nl) and [Sphinx](https://sphinx-doc.org) integration tool.

It is an easy-to-use cli tool and typically runs right after Doxygen generation.
It reuses the Doxygen generated HTML output and integrates it into Sphinx document generation.
With this, Doxysphinx supports all known Doxygen features and at the same time integrates well with the Sphinx output (for example, Sphinx-Themes, search etc.). Doxysphinx, also supports restructured text (rST) annotations within C++ files.

Internally, Doxysphinx creates an rST file for each (Doxygen) HTML file and includes the HTML using `.. raw:: html` directive.
Later Sphinx picks up these rST files and creates an integrated documentation.

### Doxysphinx vs Breathe vs Exhale

Doxysphinx is more related to [Exhale](https://exhale.readthedocs.io/en/latest/index.html) in its functionality than to [Breathe](https://breathe.readthedocs.io/en/latest/).

Breathe is useful for smaller C++ projects when parts of C++ Doxygen documentation needs to be integrated into the Sphinx documentation using [Breathe directives](https://breathe.readthedocs.io/en/latest/directives.html).
When the complete C++ Doxygen documentation needs to be integrated into Sphinx, the following options are available:

* [Breathe](https://breathe.readthedocs.io/en/latest/) + [breathe.apidoc](https://github.com/michaeljones/breathe/blob/master/breathe/apidoc.py)
* [Exhale](https://exhale.readthedocs.io/en/latest/index.html)
* Doxysphinx

Doxysphinx outperforms the other two options w.r.t to speed and features, as it simply reuses doxygen output.

## Links

📚 [Doxysphinx Overview](https://boschglobal.github.io/doxysphinx)

🚀 [Getting Started](https://boschglobal.github.io/doxysphinx/docs/getting_started.html)

💻 [Developer Quickstart](https://boschglobal.github.io/doxysphinx/docs/dev_guide.html)

🤖 [Releases](https://github.com/boschglobal/doxysphinx/releases)
