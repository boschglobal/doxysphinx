# Rst Inline Syntax

For creating inline restructured text content in C++ documentation comments that will be rendered by Sphinx.

## TLDR; Recommended Syntax

Use the following syntax in your C++ documentation comments to use a sphinx role in-line (note that you have
to replace the backticks usually used in rst/sphinx with quotes):

```cpp
/// lorem ipsum, `:role:"content of the role"` dolor sit...
```

e.g.

```cpp
/// Here you can find the `:doc:"Main Documentation <index>"`. Please read it carefully.
```

This will work only if markdown support is activated in doxygen (highly recommended).

Futhermore, please note that **you can only use sphinx roles and domains** in the inline syntax for now
(reasoning see below).

See below in the methods documentation for other options if you have markdown support disabled.

## Technical Details

Skip this section if you're not interested in the technical details...

Inline rst is a major problem because of the following:

1. **Paragraphs all over the place**

   Doxygen uses paragraphs (`<p>`-html-tags) for it's content. Paragraph tags cannot have other block-level
   tags inside them (even no other paragraph tags). The browsers (chromium-based ones, Firefox etc.) are quite
   aggressive in fixing bad nestings here (just to be able to display a page). So e.g. if a nested `<p>`-tag
   is noticed the browsers will close the outer `<p>`-tag right before the inner `<p>`-tag. This will linearize
   the `<p>`-tags and the page could be rendered.

   When we now split our content for mixed rst content as described in `:doc:"/docs/inner_workings"` we end
   up having raw-html blocks and inline-rst blocks (and also other rst blocks but that doesn't matter here).
   Sphinx will automagically put `<p>`-tags around the inline-rst-block - it's doing that around all pure
   text based content and we cannot change that.

   Most of the time this results in an html structure with nested `<p>`-tags which will be "fixed" by the
   browsers on loading/rendering of the html page. Why is this a problem? because we cannot style
   (in a css sense) away the blockiness if we have only sibling `<p>`-tags. But we have to for the content
   to appear "in-line".
   Also we cannot fix the final html structure because we're too early in the process. We can only create rsts
   which will then be picked up by sphinx to create the final html.

2. **Doxygen interpretation/preprocessing**

   The main use case for inline rst are sphinx roles which are normally (in rst) written in a form like:

   ```rst
   :role_name:`role_content`
   ```

   but doxygens internal markdown support will parse the backticks as markdown inline code block and renders
   code-tags all over the place then.

the following solutions/hacks have been applied to overcome the problems:

1. **Html-Element-Transformation**

   If we encounter a sphinx role in doxysphinx during original doxygen html parsing we change it's
   parent html tag from `<p>`-tag to `<div>`-tag (because divs can have nested content). We also add a css
   class which we use to style the "blockiness" away (display:inline). The technical implementation is
   has more complexity - if you're interested just look into the code.

2. **Adjusted Syntax for using inline rst and special parsing**

   Doxysphinx scans the html for `<code>`-tags but that's not enough. For doxysphinx to consider a `<code>`-tag as inline
   sphinx snippet it has to be in the format ``<code>:role:`content`</code>`` - we validate the syntax here and if it doesn't match we ignore it.
   The implication is that **you cannot use anything other than roles/domains for inline rst**. In practice this
   means that you cannot use rst's external link syntax and references for now, which is however so cryptic that
   we're quite sure that you would rather consider using doxygens link command or just a markdown link.

   Furthermore backticks are also markdown's verbatim inline delimiters and therefore can only be used when escaped (and even then they create problems with doxygen's way of parsing).
   Therefore we're also supporting (and are recommending) quotes (") and ticks (') as role content delimiters.
   So we relaxed the sphinx syntax a little bit here to work better in doxygen comments.

## Supported rst inline delimiters in doxygen comments

Technically doxysphinx searches for `<pre>`- or `<div class="fragment">`-elements in doxygen html output
because these are the elements it uses for verbatim code block content. There are several ways in doxygen to
create these kind of elements:

### markdown inline block

You can use markdown inline code syntax:

```cpp
/// A markdown inline statement with quotes like this - `:doc:"Main Documentation <index>"` - will work.
```

```{warning}
The role content delimiter has to be a quote ("). Ticks and escaped backticks won't work with markdown inline
code syntax because of doxygens parser.
```

### `<code>`-html-element

You can also use a html `<code>`-element:

```cpp
/// A html code element with quotes like this - <code>:doc:"Main Documentation <index>"</code> - will work.
///
/// A html code element with ticks like this - <code>:doc:'Main Documentation <index>'</code> - will work.
///
/// A html code element with escaped backticks like this - <code>:doc:\`Main Documentation <index>\`</code> - will work.
```

### `<tt>`-html-element

You can also use a html `<tt>`-element:

```cpp
/// A html tt element with quotes like this - <tt>:doc:"Main Documentation <index>"</tt> - will work.
///
/// A html tt element with ticks like this - <tt>:doc:'Main Documentation <index>'</tt> - will work.
///
/// A html tt element with escaped backticks like this - <tt>:doc:\`Main Documentation <index>\`</tt> - will work.
```

## More examples

can be found in our demo documentation [here](../doxygen/demo/html/classdoxysphinx_1_1doxygen_1_1InlineRst.rst).
