# syntax=docker/dockerfile:1

# Set the DOCKER_TAG to install
ARG DOCKER_TAG=27.3.1-cli

# Set the POETRY_VERSION to install
ARG POETRY_VERSION=1.8

# Set the PYTHON_VERSION to install
ARG PYTHON_VERSION=3.10

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/docker-python:docker__${DOCKER_TAG}--python__${PYTHON_VERSION} AS prod

USER user

ARG POETRY_VERSION

# Set poetry version environment variable
ENV POETRY_VERSION=${POETRY_VERSION}.*

# Install Poetry
RUN pip install --upgrade pip \
    && pip install --user "poetry==${POETRY_VERSION}"

# Set the environment variables for Poetry
ENV PATH=/home/user/.local/bin:$PATH

# Disable virtualenv creation
RUN poetry config virtualenvs.create false

USER root

#################### DEV IMAGE with non-root user ################

FROM ismailbouajaja/docker-python:docker__${DOCKER_TAG}--python__${PYTHON_VERSION}--dev AS dev

USER user

ARG POETRY_VERSION

# Set poetry version environment variable
ENV POETRY_VERSION=${POETRY_VERSION}.*

# Install Poetry
RUN pip install --upgrade pip \
    && pip install --user "poetry==${POETRY_VERSION}"

# Set the environment variables for Poetry
ENV PATH=/home/user/.local/bin:$PATH

# Enable virtualenv creation
RUN poetry config virtualenvs.path /home/user/.venvs

USER root
