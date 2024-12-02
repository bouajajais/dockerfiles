# syntax=docker/dockerfile:1

# Set the CUDA version to install
ARG CUDA_TAG=12.6.2-cudnn-devel-ubuntu22.04

# Set the POETRY_VERSION to install
ARG POETRY_VERSION=1.8

# Set the Python version to install
ARG PYTHON_VERSION=3.10

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/cuda-python:nvidia__cuda__${CUDA_TAG}--python__${PYTHON_VERSION} AS prod

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

FROM ismailbouajaja/cuda-python:nvidia__cuda__${CUDA_TAG}--python__${PYTHON_VERSION}--dev AS dev

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