# How to Contribute

First of all, thanks for considering contributing to this project!! Your help is highly appreciated!!

## TLDR

So this document got quite long... here is the very short summary/checklist:

* [ ] don't commit on main - use [pull requests only](#pull-requests-only)
* [ ] use this [branch naming convention](#branch-naming-convention): `feature/#39_bring_the_unicorns_back`
* [ ] commits must adhere to the [conventional commits](#conventional-commits) spec.
* [ ] add copyright header to new file or add yourself as author in existing files.
* [ ] sign your commits with a developer certificate of origin (dco) - (`git commit -s -m "MESSAGE"`) or use
      vscode which is configured for the repo to do this automatically.
* [ ] only once: add yourself as a contributor to
      [NOTICE.md](https://github.com/boschglobal/doxysphinx/blob/main/NOTICE.md).

## Pull requests only

Use pull requests to contribute to this repository.

Pushes to the `main` branch are automatically rejected.

Keep your PRs focussed on a single purpose.
For example, do not implement multiple features or fix multiple bugs in a single PR unless they are interconnected.
Simply create separate PRs instead.

## Branch naming convention

Branches should be named with this scheme:

```text
group/short_description
```

The `group` denotes the purpose of the contribution:

* **feature**: A new feature
* **fix**: A bug fix
* **ci**: GitHub workflow only changes
* **docs**: Documentation only changes

The `short` description should describe the change/feature etc.
If you have a bigger change please create an issue here in github and use the number as short description,
e.g. `feature/#39_bring_the_unicorns_back`

## Conventional Commits

We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) to automatically calculate the
semantic version, create the changelog, and publish the release via
[Python-Semantic-Release](https://python-semantic-release.readthedocs.io/en/latest/) tooling.

The following is a slightly adapted version (to doxysphinx) of the excellent
[Angular commit style](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits).

### Commit message format

Each commit message consists of a **header**, a **body** and a **footer**. The header has a special
format that includes a **type**, a **scope** and a **subject**:

```text
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The **header** is mandatory and the **scope** of the header is optional.

Any line of the commit message should not be longer than **100 characters!**.
This allows the message to be easier to read on GitHub as well as in various git tools.

### Type

Must be one of the following:

* **feat**: A new feature
* **fix**: A bug fix
* **docs**: Documentation only changes
* **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing
  semi-colons, etc)
* **refactor**: A code change that neither fixes a bug nor adds a feature
* **perf**: A code change that improves performance
* **test**: Adding missing or correcting existing tests
* **chore**: Changes to the build process or auxiliary tools and libraries such as documentation
  generation

### Scope

The scope could be anything specifying place of the commit change. For example `parser`,
`writer`, `config`, `examples`, `cli` etc...

You can use `*` when the change affects more than a single scope or just leave `(<scope>)` out completely.

### Subject

The subject contains succinct description of the change:

* use the imperative, present tense: "change" not "changed" nor "changes"
* don't capitalize first letter
* no dot (.) at the end

### Body

Just as in the **subject**, use the imperative, present tense: "change" not "changed" nor "changes".
The body should include the motivation for the change and contrast this with previous behavior.

### Footer

The footer should contain any information about **Breaking Changes** and is also the place to
[reference GitHub issues that this commit closes](https://help.github.com/articles/closing-issues-via-commit-messages/).

**Breaking Changes** should start with the word `BREAKING CHANGE:` with a space or two newlines.
The rest of the commit message is then used for this.

### Reverting a commit

If the commit reverts a previous commit, it should begin with `revert:`, followed by the header of the
reverted commit.
In the body it should say: `This reverts commit <hash>.`, where the hash is the SHA of the commit being reverted.

### Examples

* a very short new feature commit message:

  ```text
  feat: add button that brings the unicorns back
  ```

* a multiple changes (just add a newline and repeat the pattern) + breaking change commit message:

  ```text
  feat(config): config file support

  Now we established our own configuration file mechanism. The previous command line argument based
  mechanism forced the users to always create a script, use makefiles etc. With the new mechanism only a
  config file needs to be given. Config can be read from yml, toml and json files. As we're often dealing with
  python projects there is also special support for pyproject.toml.

  fixes #59

  BREAKING CHANGE: cli arguments aren't supported anymore.

  docs(config): document config mechanism

  The new config mechanism is documentation in our sphinx documentation.
  ```

## Legal stuff

### Add / retain copyright notices

Include a copyright notice and license consistent with the style used by this project.
If your contribution contains code under the copyright of a third party, document its origin, license,
and copyright holders.

Typically for code this would be through a header. You can use this as a template:
[.copyright.tmpl](.copyright.tmpl)

### Sign your work

This project also tracks patch provenance and licensing using the Developer Certificate of Origin and
Signed-off-by tags initially developed by the Linux kernel project.

```text
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
1 Letterman Drive
Suite D4700
San Francisco, CA, 94129

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

With the sign-off in a commit message you certify that you authored the
patch or otherwise have the right to submit it under an open source
license. The procedure is simple: To certify above Developer's
Certificate of Origin 1.1 for your contribution just append a line

```text
Signed-off-by: Random J Developer <random@developer.example.org>
```

to every commit message using your real name or your pseudonym and a valid
email address.

If you have set your `user.name` and `user.email` git configs you can
automatically sign the commit by running the git-commit command with the
`-s` option.  There may be multiple sign-offs if more than one developer
was involved in authoring the contribution.

### Individual vs. Corporate Contributors

Often employers or academic institution have ownership over code that is
written in certain circumstances, so please do due diligence to ensure that
you have the right to submit the code.

If you are a developer who is authorized to contribute to Ontology Central on behalf of
your employer, then please use your corporate email address in the
Signed-off-by tag, otherwise use a personal email address.

### Maintain Copyright holder / Contributor list

Each contributor is responsible for identifying themselves in the
[NOTICE.md](https://github.com/boschglobal/doxysphinx/blob/main/NOTICE.md)
file, the project's list of copyright holders and authors. Please add
the respective information corresponding to the Signed-off-by tag as
part of your first pull request.

If you are a developer who is authorized to contribute to Ontology Central on
behalf of your employer, then add your company / organization to the
list of copyright holders in the
[NOTICE.md](https://github.com/boschglobal/doxysphinx/blob/main/NOTICE.md) file. As author of a corporate
contribution you can also add your name and corporate email address as
in the Signed-off-by tag.

If your contribution is covered by this project's DCO's clause "(c) The
contribution was provided directly to me by some other person who
certified (a), (b) or (c) and I have not modified it", please add the
appropriate copyright holder(s) to the [NOTICE.md](NOTICE.md) file as part of your
contribution.

[SubmittingPatches]:
https://github.com/wking/signed-off-by/blob/7d71be37194df05c349157a2161c7534feaf86a4/Documentation/SubmittingPatches
