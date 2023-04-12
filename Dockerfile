##
## =====================================================================================
##  C O P Y R I G H T
## -------------------------------------------------------------------------------------
##  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
##
##  Author(s):
##  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
## =====================================================================================
##

FROM python:3-slim

ARG VARIANT=3.10
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

LABEL maintainer="Bosch Docs as Doxysphinx <https://github.com/boschglobal/doxysphinx>"

RUN useradd -ms /bin/bash doxysphinx_user

# set environment
ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Berlin
ENV PATH="/home/vscode/.local/bin:${PATH}"

# set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install dart-sass (needed for scoping css files to specific html elements)
RUN curl -sSL https://github.com/sass/dart-sass/releases/download/1.49.7/dart-sass-1.49.7-linux-x64.tar.gz | \
    tar -xzvf - --strip-components=1 -C /home/vscode/.local/bin dart-sass/sass

COPY dist/*.whl /app
RUN pip install *.whl

CMD [ "doxysphinx" ]
