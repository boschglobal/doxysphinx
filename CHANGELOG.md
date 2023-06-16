<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
=====================================================================================
-->

# Changelog

<!--next-version-placeholder-->

## v3.3.4 (2023-06-16)

### Fix

- **resources**: writing compiled css as utf-8 now

## v3.3.3 (2023-04-27)

### Fix

- Encoding issues on windows

## v3.3.2 (2023-04-27)

### Fix

- check if doxygen.css exists before pre-processing

## v3.3.1 (2023-04-27)

### Fix

- **toc**: Fix illegal characters in structural dummy titles

## v3.3.0 (2023-04-20)

### Feat

- **prerequisites**: dartsass isn't needed anymore because we switched to libsass

### Fix

- **styling**: fixes doxygen page headings
- **parser**: removed annotated.html from parsing exclusion list
- **resourceprovision**: fixed caching not working for stylesheets
- **devcontainer**: fixed devcontainer which was broken on first run.
- **pre-commit**: reactivated conventional commit checking

### Refactor

- fix for flake8 error C418 in toc.py

### Perf

- improve performance by parallelizing work over available cores
- improve performance by better preselection
- improved performance of json loading by an order of magnitude

## v3.2.3 (2023-04-06)

### Fix

- **doxygen_cwd**: Interpret paths relative to working dir

## v3.2.2 (2023-04-06)

### Fix

- **doxygen**: Don't launch doxygen from a shell

## v3.2.1 (2023-02-28)

### Fix

- **rst_indent_warning**: Fixed rst indent warning

## v3.2.0 (2023-02-16)

### Feat

- **code**: Removed emptyspaces before creating hash
- **incremental_behaviour**: added incremental behaviour for doxysphinx

## v3.1.0 (2022-12-09)

### Feat

- **parser**: Now rst inline syntax is supported for sphinx roles and domains.

### Fix

- **parser**: fixed doxygen comment parsing

## v3.0.0 (2022-11-18)

## v2.3.7 (2022-10-17)

### Fix

- **deps**: pyparsing dependency is added correctly now
- **doxygen**: solve pre-commit errors by whitespaces
- **doxygen**: fix errors in validator pytest
- **doxygen**: adapt optional settings for doxyfile and documentation

## v2.3.6 (2022-09-09)

### Fix

- **styling**: moved rtd style fixes to doxysphinx

## v2.3.5 (2022-09-09)

### Fix

- **doxygen**: fix warning for wrong outdir
- **doxygen**: correct the handling of relative paths and adjust pytests
- **doxygen**: add parser for doxygen config
- **validator**: fix small bug that broke build command
- **validator**: adapt error messages of validator
- **validator**: switch some settings to optional
- **doxygen**: merge current changes from global repo
- **doxygen**: respect include-tags in doxyfile

## v2.3.4 (2022-07-29)

### Fix

- **validator**: fix small bug that broke build command
- **validator**: adapt error messages of validator
- **validator**: switch some settings to optional

## v2.3.3 (2022-07-28)

### Fix

- **ci**: commit to bump version and force a release

## v2.3.2 (2022-07-27)

### Fix

- **ci**: commit to bump version and force a release

## v2.3.1 (2022-07-27)

### Fix

- **ci**: commit to bump version and force a release

## v2.3.0 (2022-07-27)

### Fix

- **ci**: commit to bump version and force a release
- **ci**: python semantic release is now parsing tags instead of commit logs

### Feat

- **cli**: direct doxygen output path specification is no possible in addition to the doxyfile

## v2.2.0 (2022-07-18)
### Feature
* **validator:** Fixed path issue in pytest ([`cb02e48`](https://github.com/boschglobal/doxysphinx/commit/cb02e489c6f3272930fee4d9d5648e8f70420183))
* **validator:** Fixed path issues in pytest. ([`38aafc9`](https://github.com/boschglobal/doxysphinx/commit/38aafc9b87615dc611b3b2924f688e15468e7533))
* **validator:** Solved errors for PR ([`f2b63bd`](https://github.com/boschglobal/doxysphinx/commit/f2b63bd92fb20842c8c5fe7d0d11cbb1618296d5))
* **validator:** Changed the validator output type. ([`9730b08`](https://github.com/boschglobal/doxysphinx/commit/9730b08a83a3ee92e3f09d4173635179f5b8e982))
* **validator:** Added a validator to check the flags of the doxyfile ([`16cf2ae`](https://github.com/boschglobal/doxysphinx/commit/16cf2ae514c09e2625cff138babfa1d7bc10e76e))

### Documentation
* **validator:** Added note to indicate ([`4a6b7b8`](https://github.com/boschglobal/doxysphinx/commit/4a6b7b82d42fe1345694c9d0f48e29a012bbc163))

## v2.1.11 (2022-06-29)
### Fix
* **styles:** Doxygens section headings and also markdown headings are now shown ([`85c062d`](https://github.com/boschglobal/doxysphinx/commit/85c062dfe34333c90871a30f2fee3d8dc8108a8a))

### Documentation
* Added a table of static doxygen page names ([`7dcdeda`](https://github.com/boschglobal/doxysphinx/commit/7dcdedac38b525d53bf4896f753cf07373d1cbcf))

## v2.1.10 (2022-06-21)
### Fix
* Remove duplicate headline ([`f12a371`](https://github.com/boschglobal/doxysphinx/commit/f12a37127b8635504a7b381a749ec8e6679c70ca))

### Documentation
* Fix sphinx_book_theme config ([`9d59320`](https://github.com/boschglobal/doxysphinx/commit/9d59320389e3cf92927c1b154357dd698695a74b))

## v2.1.9 (2022-06-01)
### Fix
* **pypi:** Pypi publishing is now active ([`86096fc`](https://github.com/boschglobal/doxysphinx/commit/86096fc3b803efeaa6fea12992cce70f4fc9c9f6))

### Documentation
* Add more status badges ([`16927d4`](https://github.com/boschglobal/doxysphinx/commit/16927d4c3192268a35e055a9dd046a30a5db4088))

## v2.1.8 (2022-06-01)
### Fix
* **ci:** Attempt to solve problem of "v" tag ([`632cd60`](https://github.com/boschglobal/doxysphinx/commit/632cd60093522f3785ad28e7dc701698c0fb0291))

## v2.1.7 (2022-06-01)


## v2.1.6 (2022-05-31)
### Fix
* **ci:** Fix typo at pypi secrets ([`77e333b`](https://github.com/boschglobal/doxysphinx/commit/77e333bf2a3eb564e97f210b8320df4d03d32b64))

## v2.1.5 (2022-05-31)
### Fix
* **ci:** Fix for really bad typo ([`aa5022d`](https://github.com/boschglobal/doxysphinx/commit/aa5022dd9c97bff90aa80b9e33c45baae2b48665))

## v2.1.4 (2022-05-30)
### Fix
* **ci:** Added precommit caching ([`5df7088`](https://github.com/boschglobal/doxysphinx/commit/5df70887f6b7dc5e3125c74e0be43d09f152a0c2))
* **ci:** Test commit to test new pypi credentials ([`c98a45a`](https://github.com/boschglobal/doxysphinx/commit/c98a45a7eab2e15a234f194235852dcd97bc7fa2))

### Documentation
* Improve readme ([`4baec67`](https://github.com/boschglobal/doxysphinx/commit/4baec6778148f162640f5b6519a1d87240276368))

## v2.1.3 (2022-05-30)
### Fix
* **ci:** Attempt to fix pypi password escaping issue ([`af5c481`](https://github.com/boschglobal/doxysphinx/commit/af5c481f464697fdaebaef3ba7a64800b58f846c))

## v2.1.2 (2022-05-30)
### Fix
* **ci:** Gitignore structure change ([`92466a3`](https://github.com/boschglobal/doxysphinx/commit/92466a3bd3231f1074408ca5786e056ba6858b8c))

## v2.1.1 (2022-05-30)
### Fix
* **ci:** Activated pypi pushing (dry-run) ([`fbd6fa8`](https://github.com/boschglobal/doxysphinx/commit/fbd6fa812fdfb4c68f87916f1202ea69222d759c))

## v2.1.0 (2022-05-23)
### Feature
* **doxygen:** Env variables in doxygen configs are now supported ([`30a6d58`](https://github.com/boschglobal/doxysphinx/commit/30a6d5869b195ef36df80a1af4dec8e2e0bef530))
* Initial contribution (internal repo hash: cea2505) ([`76dee42`](https://github.com/boschglobal/doxysphinx/commit/76dee4240394d23bf48fe5bba0bebf2f3902104c))

### Fix
* **dependencies:** Fixed missing dependency and updated all ([`27fc21d`](https://github.com/boschglobal/doxysphinx/commit/27fc21d5ef3bb6eadfc600af59d390562f4635e5))

### Documentation
* Add segmentation overview picture to inner workings. ([`05237c3`](https://github.com/boschglobal/doxysphinx/commit/05237c316f402c50c3561cac6948b66a3e046536))
* Some additions to faq on contributing images ([`d41ed11`](https://github.com/boschglobal/doxysphinx/commit/d41ed119d6115d87ec1615932b56bfe5f607671b))
