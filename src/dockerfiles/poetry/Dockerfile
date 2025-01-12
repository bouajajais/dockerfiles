# syntax=docker/dockerfile:1

# Set the POETRY_VERSION to install
ARG POETRY_VERSION=1.8

# Set the PYTHON_TAG to install
ARG PYTHON_TAG=3.10-slim

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/python:python__${PYTHON_TAG} AS prod

ARG POETRY_VERSION

# Set poetry version environment variable
ENV POETRY_VERSION=${POETRY_VERSION}.*

# Install Poetry
RUN pip install --upgrade pip \
    && pip install "poetry==${POETRY_VERSION}"

# Disable virtualenv creation for root and user
RUN poetry config virtualenvs.create false
USER user
RUN poetry config virtualenvs.create false
USER root

#################### DEV IMAGE with non-root user ################

FROM ismailbouajaja/python:python__${PYTHON_TAG}--dev AS dev

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

#################### ALPINE-PROD IMAGE with non-root user ####################

FROM ismailbouajaja/python:python__${PYTHON_TAG}--alpine-prod AS alpine-prod

ARG POETRY_VERSION

# Set poetry version environment variable
ENV POETRY_VERSION=${POETRY_VERSION}.*

# Install Poetry
RUN pip install --upgrade pip \
    && pip install "poetry==${POETRY_VERSION}"

# Disable virtualenv creation for root and user
RUN poetry config virtualenvs.create false
USER user
RUN poetry config virtualenvs.create false
USER root

#################### ALPINE-DEV IMAGE with non-root user ################

FROM ismailbouajaja/python:python__${PYTHON_TAG}--alpine-dev AS alpine-dev

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