FROM python:3.11.4-slim-bookworm as base

# Change default shell to bash, instead of sh
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV SHELL /bin/bash

# Install poetry
ENV POETRY_VERSION 1.5.1
ENV POETRY_HOME /etc/poetry
RUN  apt-get update \
        && apt-get install --no-install-recommends -y curl \
        && curl -sSL https://install.python-poetry.org | python3 \
        && apt-get autoremove -y curl \
        && apt-get clean \
        && rm -rf /var/lib/apt-get/lists/*
# Make poetry available in PATH
ENV PATH "${POETRY_HOME}/bin:${PATH}"

FROM base as dev
# The following is needed to create a user, with same uid, gid and home as host user
# This is easier for dev, VS Code inside container, and so on
# https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user
ARG USERNAME=jedi
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG HOME_DIR=/home/jedi

# Create the user
# Also, install docker, and some tools, nano and openssh-client are required for git usage
# libenchant-2-2 for spelling check
RUN groupadd --gid $USER_GID $USERNAME \
        && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -d $HOME_DIR \
        && apt-get update \
        && apt-get install --no-install-recommends -y \
        openssh-client \
        bash-completion \
        git \
        sudo \
        nano \
        libenchant-2-2 \
        && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
        && chmod 0440 /etc/sudoers.d/$USERNAME \
        && apt-get autoremove -y\
        && apt-get clean \
        && rm -rf /var/lib/apt-get/lists/*

# Switch to new user
USER ${USERNAME}