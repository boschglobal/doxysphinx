// =====================================================================================
// C O P Y R I G H T
// -------------------------------------------------------------------------------------
//  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
//
//  Author(s):
//  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
// =====================================================================================
#ifndef DEMO__COMMENT_STYLES_INCLUDED
#define DEMO__COMMENT_STYLES_INCLUDED

namespace doxysphinx
{
/// @rst
/// .. component:: doxygen_demo
///    :id: COMP_1
///    :status: done
///
///    The doxygen demo checks for the different supported comment styles in doxygen.
/// @endrst
namespace doxygen
{

/// @brief Demonstration of doxygen comment style usage. See also `:doc:"Comment Syntax Documentation </docs/syntax/comment_styles_syntax>"`.
///
class CommentStyles
{
  public:
    /**
     *\verbatim embed:rst
     *.. admonition:: What you should see here
     *
     *   This text should be in an admonition box. It was generated from a doxygen javadoc comment **without any special identation**.
     *
     *   *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*
     *
     *   .. code:: cpp
     *
     *      /**
     *       * \ verbatim embed:rst
     *       *
     *       * ...rst-content-here...
     *       *
     *       * \ endverbatim
     *       *\/
     *       void ensure_javadoc_style_comments_are_working_as_expected() const = 0;
     *
     *\endverbatim
     *
     */
    void ensure_javadoc_style_comments_are_working_as_expected() const = 0;

    /**
     *\verbatim embed:rst
     *    .. admonition:: What you should see here
     *
     *       This text should be in an admonition box. It was generated from a doxygen javadoc comment **with the rst content indented**.
     *
     *       *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*
     *
     *       .. code:: cpp
     *
     *          /**
     *           * \ verbatim embed:rst
     *           *
     *           *     ...rst-content-here...
     *           *
     *           * \ endverbatim
     *           *\/
     *           void ensure_javadoc_style_comments_with_identation_are_working_as_expected() const = 0;
     *
     *\endverbatim
     *
     */
    void ensure_javadoc_style_comments_with_identation_are_working_as_expected() const = 0;

    /**
     \verbatim embed:rst
     .. admonition:: What you should see here

        This text should be in an admonition box. It was generated from a doxygen javadoc comment **without any special identation**.

        *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*

        .. code:: cpp

           /**
            \ verbatim embed:rst

             ...rst-content-here...

            \ endverbatim
            *\/
            void ensure_javadoc_style_without_stars_are_working_as_expected() const = 0;

     \endverbatim

     */
    void ensure_javadoc_style_without_stars_are_working_as_expected() const = 0;


    /*!
     *\verbatim embed:rst
     *.. admonition:: What you should see here
     *
     *   This text should be in an admonition box. It was generated from a doxygen qt comment **without any special identation**.
     *
     *   *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*
     *
     *   .. code:: cpp
     *
     *      /*!
     *       * \ verbatim embed:rst
     *       *
     *       * ...rst-content-here...
     *       *
     *       * \ endverbatim
     *       *\/
     *       void ensure_qt_style_comments_are_working_as_expected() const = 0;
     *
     *\endverbatim
     *
     */
    void ensure_qt_style_comments_are_working_as_expected() const = 0;

    /*!
     *\verbatim embed:rst
     *    .. admonition:: What you should see here
     *
     *       This text should be in an admonition box. It was generated from a doxygen qt comment **with the rst content indented**.
     *
     *       *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*
     *
     *       .. code:: cpp
     *
     *          /*!
     *           * \ verbatim embed:rst
     *           *
     *           *     ...rst-content-here...
     *           *
     *           * \ endverbatim
     *           *\/
     *           void ensure_qt_style_comments_with_identation_are_working_as_expected() const = 0;
     *
     *\endverbatim
     *
     */
    void ensure_qt_style_comments_with_identation_are_working_as_expected() const = 0;

    /*!
     \verbatim embed:rst
     .. admonition:: What you should see here

        This text should be in an admonition box. It was generated from a doxygen qt comment **without any special identation**.

        *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*

        .. code:: cpp

           /*!
            \ verbatim embed:rst

             ...rst-content-here...

            \ endverbatim
            *\/
            void ensure_qt_style_without_stars_are_working_as_expected() const = 0;

     \endverbatim
     */
    void ensure_qt_style_without_stars_are_working_as_expected() const = 0;


    /// \verbatim embed:rst
    /// .. admonition:: What you should see here
    ///
    ///    This text should be in an admonition box. It was generated from a doxygen slash comment **without any special identation**.
    ///
    ///    *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*
    ///
    ///    .. code:: cpp
    ///
    ///       /// \ verbatim embed:rst
    ///       ///
    ///       /// ...rst-content-here...
    ///       ///
    ///       /// \ endverbatim
    ///       void ensure_slash_style_comments_are_working_as_expected() const = 0;
    ///
    /// \endverbatim
    void ensure_slash_style_comments_are_working_as_expected() const = 0;

    /// \verbatim embed:rst:leading-asterisk
    /// .. admonition:: What you should see here
    ///
    ///    This text should be in an admonition box. It was generated from a doxygen slash comment **without any special identation but with asterisk embed command**.
    ///
    ///    *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*
    ///
    ///    .. code:: cpp
    ///
    ///       /// \ verbatim embed:rst:leading-asterisk
    ///       ///
    ///       /// ...rst-content-here...
    ///       ///
    ///       /// \ endverbatim
    ///       void ensure_slash_style_comments_with_asterisk_are_working_as_expected() const = 0;
    ///
    /// \endverbatim
    void ensure_slash_style_comments_with_asterisk_are_working_as_expected() const = 0;

    /// \verbatim embed:rst
    ///     .. admonition:: What you should see here
    ///
    ///        This text should be in an admonition box. It was generated from a doxygen slash comment **with the rst content indented**.
    ///
    ///        *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*
    ///
    ///        .. code:: cpp
    ///
    ///           ///
    ///           /// \ verbatim embed:rst
    ///           ///
    ///           ///     ...rst-content-here...
    ///           ///
    ///           /// \ endverbatim
    ///           ///
    ///           void ensure_slash_style_comments_with_identation_are_working_as_expected() const = 0;
    ///
    /// \endverbatim
    void ensure_slash_style_comments_with_identation_are_working_as_expected() const = 0;

    //! \verbatim embed:rst
    //! .. admonition:: What you should see here
    //!
    //!    This text should be in an admonition box. It was generated from a doxygen slash comment **with exclamationmarks instead of the third slash**.
    //!
    //!    *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*
    //!
    //!    .. code:: cpp
    //!
    //!       //! \ verbatim embed:rst
    //!       //!
    //!       //!  ...rst-content-here...
    //!       //!
    //!       //! \ endverbatim
    //!       void ensure_slash_style_with_exclamations_are_working_as_expected() const = 0;
    //!
    //! \endverbatim
    void ensure_slash_style_with_exclamations_are_working_as_expected() const = 0;

}
}

}
#endif
