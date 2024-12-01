# syntax=docker/dockerfile:1

# Set the POETRY_VERSION to install
ARG POETRY_VERSION=1.8.*

# Set the PYTHON_TAG to install (for non-docker builds)
ARG PYTHON_TAG=3.10-slim

# Set the PYTHON_VERSION to install (for docker builds)
ARG PYTHON_VERSION=3.10

# Set the DOCKER_TAG to install
ARG DOCKER_TAG=27.3.1-cli

#################### BASE IMAGE with non-root user ####################

FROM ismailbouajaja/python:${PYTHON_TAG} AS base

ARG POETRY_VERSION

# Set poetry version environment variable
ENV POETRY_VERSION=${POETRY_VERSION}

# Install Poetry
RUN pip install --upgrade pip \
    && pip install "poetry==${POETRY_VERSION}"

# Disable virtualenv creation for root and user
RUN poetry config virtualenvs.create false
USER user
RUN poetry config virtualenvs.create false
USER root

#################### DEV BASE IMAGE with non-root user ################

FROM ismailbouajaja/python:${PYTHON_TAG}--dev AS dev-base

USER user

ARG POETRY_VERSION

# Set poetry version environment variable
ENV POETRY_VERSION=${POETRY_VERSION}

# Install Poetry
RUN pip install --upgrade pip \
    && pip install --user "poetry==${POETRY_VERSION}"

# Set the environment variables for Poetry
ENV PATH=/home/user/.local/bin:$PATH

# Enable virtualenv creation
RUN poetry config virtualenvs.path /home/user/.venvs

USER root

#################### DOCKER BASE IMAGE with non-root user and docker installed ####################

FROM ismailbouajaja/python:${PYTHON_VERSION}--docker-${DOCKER_TAG} AS docker-base

USER user

ARG POETRY_VERSION

# Set poetry version environment variable
ENV POETRY_VERSION=${POETRY_VERSION}

# Install Poetry
RUN pip install --upgrade pip \
    && pip install --user "poetry==${POETRY_VERSION}"

# Set the environment variables for Poetry
ENV PATH=/home/user/.local/bin:$PATH

# Disable virtualenv creation
RUN poetry config virtualenvs.create false

USER root

#################### DEV DOCKER BASE IMAGE with non-root user and docker installed ################

FROM ismailbouajaja/python:${PYTHON_VERSION}--dev-docker-${DOCKER_TAG} AS dev-docker-base

USER user

ARG POETRY_VERSION

# Set poetry version environment variable
ENV POETRY_VERSION=${POETRY_VERSION}

# Install Poetry
RUN pip install --upgrade pip \
    && pip install --user "poetry==${POETRY_VERSION}"

# Set the environment variables for Poetry
ENV PATH=/home/user/.local/bin:$PATH

# Enable virtualenv creation
RUN poetry config virtualenvs.path /home/user/.venvs

USER root
