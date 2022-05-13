##
## =====================================================================================
##  C O P Y R I G H T
## -------------------------------------------------------------------------------------
##  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
##
##  Author(s):
##  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
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
ENV PATH="/home/vscode/.local/bin:${PATH}"

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

# Install plantUML
RUN wget -c https://netcologne.dl.sourceforge.net/project/plantuml/plantuml.jar -O /tmp/plantuml.jar && \
    mkdir -p /usr/share/plantuml && \
    mv /tmp/plantuml.jar /usr/share/plantuml/plantuml.jar

# Switch to vscode user
USER vscode

# Install poetry (as vscode so that poetry is installed in the correct home directory)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install dart-sass (needed for scoping css files to specific html elements)
RUN curl -sSL https://github.com/sass/dart-sass/releases/download/1.49.7/dart-sass-1.49.7-linux-x64.tar.gz | \
    tar -xzvf - --strip-components=1 -C /home/vscode/.local/bin dart-sass/sass

# configure poetry completion
RUN poetry completions zsh > ~/.oh-my-zsh/plugins/poetry/_poetry

# note that installation of dependencies and pre-commit installation will be done after vscode has started
# the container.
