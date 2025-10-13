# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

import os
from pathlib import Path
import shutil

from click.testing import CliRunner

from doxysphinx.cli import cli
from doxysphinx.utils.pathlib_fix import path_resolve


def test_build_is_working_as_expected():
    """Check if the build is working as expected"""
    runner = CliRunner()
    repo_root = path_resolve(Path())

    sphinx_source = repo_root
    sphinx_output = repo_root / ".build/html"
    doxyfile = repo_root / "demo" / "demo.doxyfile"

    result = runner.invoke(
        cli,
        [
            "--verbosity=DEBUG",
            "build",
            str(sphinx_source),
            str(sphinx_output),
            str(doxyfile),
        ],
    )
    assert (repo_root / "pyproject.toml").exists()
    if result.exit_code != 0:
        print("Build had errors - std output stream:")
        print(result.stdout)
    assert result.exit_code == 0
    assert (repo_root / ".build/html/docs/doxygen/demo/html/doxygen.css").exists()


def test_longpath_build():
    """Test building with long paths"""
    runner = CliRunner()
    repo_root = path_resolve(Path())

    # Copy our demo directory to a very long path
    # The path needs to be over 255 characters long to trigger issues on Windows
    # Windows has a max path length of 255 characters by default
    # (see https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation)
    long_dir_name = "a" * 250  # Single very long directory name
    long_path = repo_root / long_dir_name

    # Test if we can create the long path at all
    if os.name == "nt":
        # On Windows, use extended-length path support
        try:
            # Use \\?\ prefix for the actual copy operation
            shutil.copytree(rf"\\?\{repo_root}", rf"\\?\{long_path}", dirs_exist_ok=True)
        except OSError as e:
            raise AssertionError(
                f"Long path copy failed on Windows - this indicates the tool won't work with long paths: {e}")
    else:
        shutil.copytree(repo_root, long_path, dirs_exist_ok=True)

    # Verify the copy worked by checking for key files
    # On Windows with long paths, use os.path.exists with \\?\ prefix for verification
    if os.name == "nt":
        assert os.path.exists(rf"\\?\{long_path}"), f"Long path directory was not created: {long_path}"
        assert os.path.exists(rf"\\?\{long_path}\pyproject.toml"), f"pyproject.toml not found in long path: {long_path}"
    else:
        assert long_path.exists(), f"Directory was not created: {long_path}"
        assert (long_path / "pyproject.toml").exists(), f"pyproject.toml not found: {long_path}"

    sphinx_source = long_path
    sphinx_output = long_path / ".build/html"
    doxyfile = long_path / "demo" / "demo.doxyfile"

    result = runner.invoke(
        cli,
        [
            "--verbosity=DEBUG",
            "build",
            "--doxygen_cwd",
            str(long_path),
            str(sphinx_source),
            str(sphinx_output),
            str(doxyfile),
        ],
    )
    if result.exit_code != 0:
        print("Build had errors - std output stream:")
        print(result.stdout)
    assert result.exit_code == 0
    # Check the final output file
    css_file_path = long_path / ".build/html/docs/doxygen/demo/html/doxygen.css"
    if os.name == "nt":
        assert os.path.exists(rf"\\?\{css_file_path}"), f"Output CSS file missing: {css_file_path}"
    else:
        assert css_file_path.exists(), f"Output CSS file missing: {css_file_path}"

    # Clean up - only if the directory was actually created
    if long_path.exists():
        if os.name == "nt":
            shutil.rmtree(rf"\\?\{long_path}")
        else:
            shutil.rmtree(long_path)


def test_worker_limiting():
    """Test that worker limiting functionality works for build and clean commands"""
    runner = CliRunner()
    repo_root = path_resolve(Path())

    sphinx_source = repo_root
    sphinx_output = repo_root / ".build/html"
    doxyfile = repo_root / "demo" / "demo.doxyfile"
    worker_limit = 4

    result = runner.invoke(
        cli,
        [
            "--verbosity=DEBUG",
            "clean",
            "--workers",
            str(worker_limit),
            str(sphinx_source),
            str(sphinx_output),
            str(doxyfile),
        ],
    )
    assert f"running in parallel with limit of {worker_limit} workers" in result.stdout

    result = runner.invoke(
        cli,
        [
            "--verbosity=DEBUG",
            "build",
            "--workers",
            str(worker_limit),
            str(sphinx_source),
            str(sphinx_output),
            str(doxyfile),
        ],
    )
    assert (repo_root / "pyproject.toml").exists()
    if result.exit_code != 0:
        print("Build had errors - std output stream:")
        print(result.stdout)
    assert result.exit_code == 0
    assert (repo_root / ".build/html/docs/doxygen/demo/html/doxygen.css").exists()
    assert f"running in parallel with limit of {worker_limit} workers" in result.stdout


def test_incremental_build_working_as_expected():
    """Check incremental behaviour"""
    runner = CliRunner()
    repo_root = path_resolve(Path())

    sphinx_source = repo_root
    sphinx_output = repo_root / ".build/html"
    doxyfile = repo_root / "demo" / "demo.doxyfile"

    result = runner.invoke(
        cli,
        [
            "--verbosity=DEBUG",
            "clean",
            str(sphinx_source),
            str(sphinx_output),
            str(doxyfile),
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        cli,
        [
            "--verbosity=DEBUG",
            "build",
            str(sphinx_source),
            str(sphinx_output),
            str(doxyfile),
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        cli,
        [
            "--verbosity=DEBUG",
            "build",
            str(sphinx_source),
            str(sphinx_output),
            str(doxyfile),
        ],
    )
    assert "created 0 rst-files" in result.stdout
