<!-- test -->
# Welcome to the Doxysphinx Demo C++ project

<!-- You can link to sphinx static content by specifing a relative path in the final output -->
<!-- ![Logo](../../../../_static/doxysphinx_logo.svg) -->

<!-- however you can also use doxygens internal linking mechanism-->
![Logo](@ref doxysphinx_logo.svg)

### Intro

This is the mainpage of the doxysphinx C++ demo sources.
It is a markdown document rendered by doxygen (not sphinx).

> If you use markdown pages in doxygen and want to reference e.g. classes you can use the special syntax
> provided by doxygen-markdown (see <https://doxygen.nl/manual/markdown.html>), e.g.
> [This is a link to the Car class](@ref doxysphinx::rst::Car).

### Linking to sections

You can also reference the doxygen sections manually like this (using final html document names):

* [Namespace List](namespaces.html)
* [Class List](annotated.html)
  * [Class Index](classes.html)
  * [Class Hierarchy](inherits.html)
  * [Class Members](functions.html)
* [Files](files.html)
