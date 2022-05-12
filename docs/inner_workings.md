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

The main entrypoint to doxysphinx is the {py:func}`doxysphinx.cli` and the commands defined in {py:func}`doxysphinx.commands`,
currently we have:

- build (which builds the rst files for doxygen)
- clean (which removes any file created from doxysphinx)

These commands take the `sphinx_source_directory` the `sphinx_output_directory` and at least one doxygen config
file (`doxyfile`) as input to do their work.

## Pipeline

Doxysphinx follows a relatively easy pipeline architecture:

- A builder is created (for now there's only one: {py:class}`DoxygenRstBuilder`)
  - This builder represents the whole rst generation/building process which has these phases
    - __Resource Provisioning__:

      In this step html resources (images, stylesheets, javascript files etc.) are copied to the output directory and
      adapted. The input and output directories are mapped with the help of a {py:class}`DirectoryMapper`
    - __Building Rst Files__:

      Each HTML file found in the doxygen output is parsed (with a {py:class}`HtmlParser`) and written to an rst file
      (with a {py:class}`Writer`).

## Rst generation

### Segmentation overview

```{image} resources/doxysphinx.drawio.svg
TODO: draw and add the image here
```

### Explanations

1. Doxygen html output is parsed
2. For each doxygen html file a rst file is created based on the following rules:
   - If the html file doesn't contain any rst documentation blocks an rst with a raw include directive is written.
     This will directly put the html file into the output (but with sphinx templating/toc etc. "around")
   - If the html file contains at least one \rst(or @rst) documentation element it is "splitted" at these
     rst documentation snippets. For each html segment a raw html directive with the html as content is then written
     and each rst segment is written directly.
   - The rst files are written in parallel to the html files with the same name but the rst suffix instead of the html
     suffix.
3. When sphinx processes these rst files it will render the results as html to it's own output directory thereby
   keeping the original file name which means that all doxygen internal links stay intact.

### Additional notes

- A custom css is provided in doxygen to do some styling cleanup (because of the different main stylesheets of doxygen
  and sphinx).
- As the sphinx raw html directive isn't considering resources (css, images, javascript-files etc.) these files are
  are copied to the output directory if they are newer (this is done at the beginning of the process).
- The tool is currently designed as "postbuild step" after doxygen. So each time doxygen runs this tool should run
  afterwards. We also considered creating a sphinx extension, however there isn't much benefit to it as of now.
