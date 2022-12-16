<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
=====================================================================================
-->

# Inner workings

Doxysphinx is a [click](https://click.palletsprojects.com/) cli application.

## Entry

The main entrypoint to doxysphinx is the {py:mod}`~doxysphinx.cli` module and the commands defined in it:

- build (which builds the rst files for doxygen)
- clean (which removes any file created from doxysphinx)

These commands take the `sphinx_source_directory` the `sphinx_output_directory` and at least one doxygen
config file (`doxyfile`) as input to do their work.

## 1000 ft view

During build command doxysphinx follows these steps:

- A builder is created (for now there's only one {py:class}`~doxysphinx.process.Builder`. But in the future
  there may be more)
- This builder represents the whole rst generation/building process which has these phases:

  - __Resource Provisioning__:

    In this step html resources (images, stylesheets, javascript files etc.) are copied to the output
    directory and adapted. The input and output directories are mapped with the help of a
    {py:class}`~doxysphinx.sphinx.DirectoryMapper`.
  - __Building Rst Files__:

    Each HTML file found in the doxygen output is parsed (with a
    {py:class}`~doxysphinx.html_parser.HtmlParser`) and written to an rst file (with a
    {py:class}`~doxysphinx.writer.Writer`).

## 100 ft view

### Overview

```{image} resources/inner_workings_segmentation_overview.svg
```

### Process

1. Doxygen html output is parsed. This is implemented in
   {py:class}`~doxysphinx.html_parser.DoxygenHtmlParser`. The Parser will parse load the html file, do some
   processing (it will extract some metadata and change `<pre>`- and `<verbatim>`-tags into more generic
   `<rst>`-tags) and creates a {py:class}`~doxysphinx.html_parser.HtmlParseResult` that contains the metadata
   and the processed DOM as an etree.
2. For each doxygen html file a rst file is created based on the following rules (see
   {py:meth}`RstWriter.write(...) <doxysphinx.writer.RstWriter.write>`):
   - If the html file doesn't contain any rst documentation blocks an rst with a raw include directive is
     written. This will directly put the html file into the output (but with sphinx templating/toc etc. "around").
   - If the html file contains at least one `\rst` (or `@rst`) documentation element it is "splitted" at these
     rst documentation snippets. For each html segment a raw html directive with the html as content is then
     written and each rst segment is written directly.
   - The rst files are written in parallel to the html files with the same name but the rst suffix instead of
     the html suffix.
   - The {py:class}`~doxysphinx.writer.RstWriter` will also create a toctree for some rsts based on the
     {py:class}`~doxysphinx.writer.DoxygenTocGenerator` implementation.
3. When sphinx processes these rst files it will render the results as html to it's own output directory
   thereby keeping the original file name which means that all doxygen internal links stay intact.

### Additional notes

- As the sphinx raw html directive isn't considering resources (css, images, javascript-files etc.) these
  files are copied to the output directory if they are newer (this is done at the beginning of the process) -
  see {py:class}`~doxysphinx.resources.DoxygenResourceProvider`.
- In the ResourceProvider we also patch the doxygen.css file via libsass to scope it below a special
  div-element ({py:meth}`~doxysphinx.writer.RstWriter.`) and add some extra css rules which change some theme
  css styles. For the scoping see {py:class}`~doxysphinx.resources.CssScoper`.

## 10 ft view

Hey, if read this far you have to be a developer - Just fire up your IDE and look into the code 😊.
