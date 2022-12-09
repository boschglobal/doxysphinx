# Comment Syntax

## Supported Doxygen Comment Styles

We're supporting the following Doxygen comment styles (see also
[Doxygen: Comment Blocks for C-Style Languages](https://doxygen.nl/manual/docblocks.html#cppblock)).

### Triple-Slashes

```cpp
/// @brief brings the unicorns back
///
/// It does that with an extraordinary special top secret device of extraterrestrial origin.
void bring_the_unicorns_back();
```

### Javadoc

```cpp
/**
 * @brief brings the unicorns back
 *
 * It does that with an extraordinary special top secret device of extraterrestrial origin.
 */
void bring_the_unicorns_back();
```

or

```cpp
/**
  @brief brings the unicorns back

  It does that with an extraordinary special top secret device of extraterrestrial origin.
 */
void bring_the_unicorns_back();
```

### Qt

```cpp
/*!
 * @brief brings the unicorns back
 *
 * It does that with an extraordinary special top secret device of extraterrestrial origin.
 */
void bring_the_unicorns_back();
```

or

```cpp
/*!
  @brief brings the unicorns back

  It does that with an extraordinary special top secret device of extraterrestrial origin.
 */
void bring_the_unicorns_back();
```

### Double-Slashes-With-Exclamation-Marks

```cpp
//! @brief brings the unicorns back
//!
//! It does that with an extraordinary special top secret device of extraterrestrial origin.
void bring_the_unicorns_back();
```
