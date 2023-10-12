<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
=====================================================================================
-->
# Commenting in doxygen

You can use rst snippets in all supported doxygen comment styles.

The rst snippets just need to be fenced with the alias tags `rst` and `endrst`. However do not nest `rst` fences. This won't work.

Depending on your preference you can use `@rst` and `@endrst` or `\rst` and `\endrst`.

Here are some examples (for further examples see {demo}`doxysphinx::doxygen::CommentStyles`).

## Javadoc Comments

### Variant A - with asterisks

```c++
/**
 *\rst
 * .. info
 *    as you can see you can just use directives and anything here
 *
 * also just normal text blocks.
 * Everything inbetween \rst and \endrst will be treated like a normal rst file.
 *\endrst
 */
 void test() const;
```

### Variant B - without asterisks

```c++
/**
 \rst
         .. admonition:: Another info

            The indentation will be normalized automatically by doxysphinx.
            However as with any other rst file you should stick to the sphinx identation rules.

 \endrst
 */
 void test() const;
```

## Qt-Style Comments

### Variant A - with asterisks

```c++
/*!
 *\rst
 * .. info
 *    Qt-style comments also work.
 *\endrst
 *\/
 void test() const;
```

### Variant B - without asterisks

```c++
/*!
 *\rst
 *      .. info
 *         Qt-style comments without asterisk and indentation also work
 *\endrst
 *\/
 void test() const;
```

## Slash Comments

### Variant A - tripple slashs (microsoft style)

```c++
/// @rst
///
/// ...rst-content-here...
///
/// @endrst
void test() const;
```

### Variant B - double slash exclamation mark

```c++
//! @rst
//!
//!         ...rst-content-here...
//!
//! @endrst
void test() const:
```
