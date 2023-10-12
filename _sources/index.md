<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
 - Aniket Salve, Robert Bosch GmbH
=====================================================================================
-->

# Overview

```{toctree}
:hidden:
:maxdepth: 1
:caption: Usage

docs/getting_started.md
docs/syntax/syntax_guide.md
docs/alternatives.md
docs/faq.md
```

```{toctree}
:hidden:
:maxdepth: 1
:caption: Examples

docs/linking_to_doxygen.md
docs/using_rst_in_doxygen.md
docs/linking_needs.md
```

```{toctree}
:hidden:
:caption: Demo documentations
:maxdepth: 1
Doxygen Demo <docs/doxygen/demo/html/index>
```

```{toctree}
:hidden:
:maxdepth: 1
:caption: Development

docs/dev_guide
docs/inner_workings.md
docs/apidoc.md
CONTRIBUTE.md
```

```{toctree}
:hidden:
:maxdepth: 1
:caption: Other stuff
```

```{toctree}
:hidden:
:maxdepth: 1
:caption: Related Topics

docs/doxylink_setup.md
```

Welcome to the Doxysphinx documentation!

## What is Doxysphinx?

### ...an integration tool

Doxysphinx is a [doxygen](https://doxygen.nl) and [sphinx](https://sphinx-doc.org) integration tool.

It will make the doxygen documentation appear inside the sphinx documentation:

````{card}
```{image} docs/resources/index_doxysphinx_example.png
:alt: doxysphinx result examples screenshot
:width: 1200px
```
````

It comes as an easy-to-use cli tool and typically runs right after doxygen created it's html documentation.
Doxysphinx creates restructured text (.rst) files out of these (doxygen) html files.
Afterwards sphinx will pick up these rst files and create an integrated documentation (sphinx theming is applied, search etc.).

```{image} docs/resources/index_doxysphinx_process.png
:alt: doxysphinx integration process
:width: 550px
```

### ...a traceability enablement tool

Doxysphinx is also a traceability enablement tool because as doxygen documentation gets integrated with sphinx
you can e.g. define and reference [sphinx-needs](https://sphinxcontrib-needs.readthedocs.io/en/latest/)
objects to link requirements, architecture elements, etc. directly in and to your source code.

With that it can be also seen as a little cog in the **docs-as-code** gear.

## Features

* Reuses doxygens html output...
  * Graphics are working (hierarchies, etc.)
  * Doxygen's structure and views are preserved - namespaces, indexes, code views etc.
* Integration in sphinx brings...
  * Sphinx Theming/Frame applied
  * Sphinx full text search over the doxygen documentation
* Use sphinx enabled (directives, extensions, etc.) restructured text snippets in doxygen comments
  * This allows for example to define and reference sphinx need objects like requirements, components etc. down
    in the source code to get full tracability.

## Caveats

* Right now doxysphinx is developed against the [sphinx-book-theme](https://sphinx-book-theme.readthedocs.io/)
  and the [sphinx-rtd-theme](https://sphinx-rtd-theme.readthedocs.io/).

  Other Themes might work but aren't styled explicitely.

* [Furo](https://pradyunsg.me/furo/quickstart/) theme will unfortunately not work because of some quality-gates
  in Furo which check for header-tags in output.
  As doxygen html has such tags and we integrate it directly it won't work with furo.

* Doxysphinx can only include complete doxygen pages. If you want to embedd e.g. a single class or method
  documentation inline in your docs please take a look at [Breathe](https://github.com/michaeljones/breathe)
  or the other [alternatives](./docs/alternatives.md).
