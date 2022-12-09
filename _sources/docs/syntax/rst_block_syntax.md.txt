# Rst Block Syntax

For creating blocks of restructured text content in C++ documentation comments that will be rendered by Sphinx.

## TLDR; Recommended Syntax

- if you want to use the shortest possible syntax use [](#markdown-fences) with directive autodetection.
- if you're coming from breathe and already have your code commented with breathe markers or if you want
  to have maximum compatibility: use [](#doxygen-aliases).

However if you experience any problems with doxygen parsing etc. you might try one of the other options described
in [](#supported-rst-block-delimiters-in-doxygen-comments).

## Markers

For doxysphinx to be able to identify a rst block we only need to have some kind of "verbatim block" in html
output and a special marker at the beginning of the content.

The marker can be one of these:

- `{rst}` -> our (doxysphinx) own marker
- `embed:rst`
- `embed:rst:leading-asterisk`
- `embed:rst:leading-slashes` -> breathe compatibility markers

After any marker there has to be a new line (content can start at next line).

### Directive Autodetection

As chances are quite big that you just want to use a sphinx directive we've also got an autodetection feature:
if the "verbatim content" starts with a directive you can leave out the markers (in that case the directive syntax is
the marker), for example...

```cpp
/// ```
/// .. directive:: title
///    DIRECTIVE CONTENT
/// ```
```

...will also be identified by doxysphinx as a rst block (and processed).

## Supported rst block delimiters in doxygen comments

Technically doxysphinx searches for `<pre>`- or `<div class="fragment">`-elements in doxygen html output
because these are the elements it uses for verbatim code block content. There are several ways in doxygen to
create these kind of elements:

### Markdown Fences

You can use the markdown code fences syntax as follows (you need to have markdown enabled in doxygen to use it):

```cpp
/// ...
///
/// ```
/// {rst}
/// enter your rst content,
/// like directives, free text rst content,
/// etc...
/// ```
///
/// ...
```

```{warning}

   In markdown it's typical to have a language identifier right behind the beginning "fence".
   Something like <code>\`\`\`cpp</code> for example. However the doxygen markdown parser will swallow anything
   behind the delimiters (which means we couldn't make use of information there). So please do not fall into
   the trap trying to start a rst block with e.g. <code>\`\`\`{rst}</code>. The `{rst}` marker (or any content
   used by doxysphinx) **has to be on the next line**. (This is only true if you use markdown code fences - not for
   the other options below).
```

### `\verbatim` special command

You can use the verbatim special command in doxygen to create a pre-element:

```cpp
/// ...
///
/// \verbatim {rst}
/// enter your rst content,
/// like directives, free text rst content,
/// etc...
/// \endverbatim
///
/// ...
```

### `<pre>`-html-element

As you can also use html in doxygen you can use the html `<pre>`-element directly:

```cpp
/// ...
///
/// <pre> {rst}
/// enter your rst content,
/// like directives, free text rst content,
/// etc...
/// </pre>
///
/// ...
```

### Doxygen aliases

As another shortcut you can also use doxygen aliases to create your own rst-block delimiters:

```text
ALIAS       =  "rst=\verbatim embed:rst"
ALIAS       += "endrst=\endverbatim"
```

And then use the alias like this:

```cpp
/// ...
///
/// \rst
/// enter your rst content,
/// like directives, free text rst content,
/// etc...
/// \endrst
///
/// ...
```

## More examples

can be found in our demo documentation [here](../doxygen/demo/html/classdoxysphinx_1_1doxygen_1_1BlockRst.rst).
