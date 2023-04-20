<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
=====================================================================================
-->
# Linking to Doxygen

:::{tip}

As you know from [Getting Started-guide](./getting_started.md) your doxygen documentation has to be created
in the SPHINX_SOURCE directory tree.

We recommend to put it under a special doxygen folder, e.g. to `docs/doxygen/<your_doxygen_module_name>` e.g.
in our repo here it lives in `docs/doxygen/demo/`.
´
When doing it that way you have a nice separation of the doxygen bits from the rest of the documentation
and you have serveral doxygen documentations in parallel (or in a sub tree structure if you like).

:::

On this page 3 possibilities are shown to link from sphinx/rst files to doxygen documentation.

## inside a toctree directive

This is typically used to integrate the doxygen documentation into your own toctree.

```````{grid} 2
:gutter: 1

``````{grid-item-card} Definition in rst/md files
`````{tab-set}
````{tab-item} rst
:sync: rst

```rst
.. absolute link to directory
.. toctree::

   /docs/doxygen/demo/html

.. relative link to directory
.. toctree::

   ../doxygen/demo/html

.. absolute link to rst file
.. toctree::

   /docs/doxygen/demo/html/index
```
````

````{tab-item} myst markdown
:sync: md

:::md
<!-- absolute link to directory -->
```{toctree}
/docs/doxygen/demo
```

<!-- relative link to directory -->
```{toctree}
../doxygen/demo
```

<!-- absolute link to rst file -->
```{toctree}
/docs/doxygen/demo/index
```
:::
````
`````
``````
``````{grid-item-card} Definition in rst/md files
just see the navigation of this document. There is a toctree link to the demo module.
``````
```````

## via document link

This is typically used to reference the root docs or some special page where you know the exact name
(Don't use it for C++ Symbols, as there are better ways to link them - see [](#via-doxylink-symbol-links)).

```````{grid} 2
:gutter: 1

``````{grid-item-card} Definition in rst/md files
`````{tab-set}
````{tab-item} rst
:sync: rst

```rst
.. absolute document link (absolute to sphinx document root dir)
:doc:`/docs/doxygen/demo/html/index`

.. relative document link (relative to the current document)
:doc:`doxygen/demo/html/index`

.. with custom caption
:doc:`C++ Demo Project Doxygen Api Documentation </docs/doxygen/demo/html/index>`
```
````

````{tab-item} myst markdown
:sync: md

```md
<!-- absolute document link (absolute to sphinx document root dir) -->
{doc}`/docs/doxygen/demo/html/index`

<!-- relative document link (relative to the current document) -->
{doc}`doxygen/demo/html/index`

<!-- with custom caption (myst or plain markdown) -->
{doc}`C++ Demo Project Doxygen Api Documentation <doxygen/demo/html/index>`

[C++ Demo Project Doxygen Api Documentation](/docs/doxygen/demo/html/index)
```
````
`````
``````

``````{grid-item-card} Output example
`````{tab-set}
````{tab-item} rst
:sync: rst

```{eval-rst}
.. absolute document link (absolute to sphinx document root dir)

:doc:`/docs/doxygen/demo/html/index`

.. relative document link (relative to the current document)

:doc:`doxygen/demo/html/index`

.. with custom caption

:doc:`C++ Demo Project Doxygen Api Documentation </docs/doxygen/demo/html/index>`
```
````

````{tab-item} myst markdown
:sync: md

<!-- absolute document link (absolute to sphinx document root dir) -->
{doc}`/docs/doxygen/demo/html/index`

<!-- relative document link (relative to the current document) -->
{doc}`doxygen/demo/html/index`

<!-- with custom caption (myst or plain markdown) -->
{doc}`C++ Demo Project Doxygen Api Documentation <doxygen/demo/html/index>`

[C++ Demo Project Doxygen Api Documentation](/docs/doxygen/demo/html/index)
````
`````
``````
```````

````{tip}
As for each doxygen html file an equally named rst file will be created by doxysphinx you can just reference
the doxygen sections via their names. However as these aren't always obvious here's a list:

| Doxygen page title | html/rst name | example link (e.g. for toctree or doc link) | rendered example |
| --- | ---   | --- | --- |
| Main Page | index | `/docs/doxygen/demo/html/index` | {doc}`/docs/doxygen/demo/html/index` |
| Namespace List | namespaces | `/docs/doxygen/demo/html/namespaces` | {doc}`/docs/doxygen/demo/html/namespaces` |
| Class List | annotated | `/docs/doxygen/demo/html/annotated` | {doc}`/docs/doxygen/demo/html/annotated` |
| Class Index | classes | `/docs/doxygen/demo/html/classes` | {doc}`/docs/doxygen/demo/html/classes` |
| Class Hierachy | inherits | `/docs/doxygen/demo/html/inherits` | {doc}`/docs/doxygen/demo/html/inherits` |
| Class Members | functions | `/docs/doxygen/demo/html/functions` | {doc}`/docs/doxygen/demo/html/functions` |
| Files | files | `/docs/doxygen/demo/html/files` | {doc}`/docs/doxygen/demo/html/files` |
````

## via doxylink symbol links

When you set up doxylink correctly (see [Doxylink Setup](doxylink_setup.md)) you can
link C++ symbols directly from your rst sources.

:::{note}
doxylink "knows" the symbols because in the doxygen tagfile all symbols are mapped to the respective html files.
:::

```````{grid} 2
:gutter: 1

``````{grid-item-card} Definition in rst/md files
`````{tab-set}
````{tab-item} rst
:sync: rst

```rst
.. namespace
:demo:`doxysphinx::rst`
.. class
:demo:`doxysphinx::rst::Car`
.. method
:demo:`doxysphinx::rst::Car::enter(Driver& driver)`
```
````

````{tab-item} myst markdown
:sync: md

```md
<!-- namespace -->
{demo}`doxysphinx::rst`
<!-- class -->
{demo}`doxysphinx::rst::Car`
<!-- method -->
{demo}`doxysphinx::rst::Car::enter(Driver& driver)`
```
````
`````
``````

``````{grid-item-card} Output example
`````{tab-set}
````{tab-item} rst
:sync: rst

```{eval-rst}
.. namespacer

:demo:`doxysphinx::rst`

.. class

:demo:`doxysphinx::rst::Car`

.. method

:demo:`doxysphinx::rst::Car::enter(Driver& driver)`
```
````

````{tab-item} myst markdown
:sync: md

<!-- namespace -->
{demo}`doxysphinx::rst`
<!-- class -->
{demo}`doxysphinx::rst::Car`
<!-- method -->
{demo}`doxysphinx::rst::Car::enter(Driver& driver)`
````
`````
``````
```````
