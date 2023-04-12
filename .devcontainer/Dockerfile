##
## =====================================================================================
##  C O P Y R I G H T
## -------------------------------------------------------------------------------------
##  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
##
##  Author(s):
##  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
##  - Stefan Schulz, itemis AG (contracted by Robert Bosch GmbH)
## =====================================================================================
##

ARG VARIANT=3.10
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

LABEL maintainer="Bosch Doxysphinx Team <https://github.com/boschglobal/doxysphinx/>"

# default shell = zsh
SHELL [ "/bin/zsh", "-c" ]

# set environment
ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Berlin
ENV PATH="/root/.local/bin:/home/vscode/.local/bin:${PATH}"

# Install apt dependencies
# - default-jre for running plantuml
# - graphviz for plantuml/doxygen (however that's already provided by the base image - still we have it here in case we'd switch..)
# - doxygen
# - imagemagick (sphinx dependency)
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install --no-install-recommends -y \
    default-jre \
    graphviz \
    doxygen \
    imagemagick \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Update doxygen to latest
RUN wget -c https://www.doxygen.nl/files/doxygen-1.9.6.linux.bin.tar.gz -O /tmp/doxygen.tar.gz \
    && mkdir -p /tmp/doxygen \
    && tar -xzvf /tmp/doxygen.tar.gz --strip-components=1 -C /tmp/doxygen/ \
    && mv /tmp/doxygen/bin/* /usr/bin \
    && mv /tmp/doxygen/man/man1/* /usr/share/man/man1 \
    && rm -rf /tmp/doxygen/

# Install plantUML
RUN wget -c https://netcologne.dl.sourceforge.net/project/plantuml/plantuml.jar -O /tmp/plantuml.jar && \
    mkdir -p /usr/share/plantuml && \
    mv /tmp/plantuml.jar /usr/share/plantuml/plantuml.jar

# Switch to vscode user
USER vscode

# set workspace dir and ensure it's present
# set cache home directory to in-repo directory (so it will survive container rebuilds and speed up startup
# and dependency resolution)
ARG WORKSPACE_DIR
WORKDIR ${WORKSPACE_DIR}/

# set cache home directory to in-repo directory (so it will survive container rebuilds and speed up startup
# and dependency resolution)
ENV XDG_CACHE_HOME=${WORKSPACE_DIR}/.cache

# Install poetry (we're not use pipx here because poetry in a virtualenv has it's issues...)
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry completions bash >> ~/.bash_completion

# Install poetry up plugin to update dependencies
RUN poetry self add poetry-plugin-up

# Install precommit globally in the container (with pipx installation we had error messages during pre-commit
# checks like "/usr/local/bin/python: No module named pre_commit" - seems it needs the python module available
# in the global python environment
RUN pip install pre-commit

# Inject + Install QA tooling
RUN pipx inject flake8 flake8-bugbear flake8-comprehensions flake8-simplify cohesion pydocstyle \
    flake8-docstrings pep8-naming \
    && pipx inject mypy lxml-stubs types-PyYAML \
    && pipx install isort \
    && pipx install safety \
    && pipx install commitizen

# install pytest
RUN pipx install pytest && pipx inject pytest pytest-cov pytest-emoji pytest-md

# install pex for packaging
RUN pipx install pex

# for pylint we would need to install c libs in it's pipx env and also whitelist them in pyproject.toml
# thats the reason why we deactivated that for now...
#RUN pipx inject pylint lxml mpire

# note that installation of dependencies and pre-commit installation will be done after vscode has started
# the container.
