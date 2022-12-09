##
## =====================================================================================
##  C O P Y R I G H T
## -------------------------------------------------------------------------------------
##  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
##
##  Author(s):
##  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
##  - Stefan Schulz, itemis AG (contracted by Robert Bosch GmbH)
## =====================================================================================
##

ARG VARIANT=3.10
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

LABEL maintainer="Bosch Doxysphinx Team <https://github.com/boschglobal/doxysphinx/>"

# default shell = zsh
SHELL [ "/bin/zsh", "-c" ]

# set environment
ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Berlin
ENV PATH="/root/.local/bin:${PATH}"

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
RUN wget -c https://www.doxygen.nl/files/doxygen-1.9.5.linux.bin.tar.gz -O /tmp/doxygen.tar.gz \
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
ARG WORKSPACE_DIR=/workspaces/
ENV XDG_CACHE_HOME=${WORKSPACE_DIR}/.cache
WORKDIR ${WORKSPACE_DIR}/

# Install poetry (as vscode so that poetry is installed in the correct home directory)
#RUN curl -sSL https://install.python-poetry.org | python3
RUN pipx install poetry \
    && pipx install poetryup \
    && pipx install pre-commit

# Install dart-sass (needed for scoping css files to specific html elements)
# Some dart-sass versions ship with a src folder, which contains the dart binary so we need to extract all
# contents of the tarball. Note that this will create a src folder in /home/vscode/.local/bin.
RUN mkdir -p /home/vscode/.local/bin && \
    export PLATFORM="$(uname -m | sed 's/aarch64/arm64/' | sed 's/86_//')" && \
    echo Installing dart-sass for $PLATFORM && \
    curl -sSL https://github.com/sass/dart-sass/releases/download/1.52.3/dart-sass-1.52.3-linux-${PLATFORM}.tar.gz | \
    tar -xzvf - --strip-components=1 -C /home/vscode/.local/bin dart-sass/


# note that installation of dependencies and pre-commit installation will be done after vscode has started
# the container.
