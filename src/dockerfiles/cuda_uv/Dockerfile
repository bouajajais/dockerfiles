# syntax=docker/dockerfile:1

# Set the CUDA version to install
ARG CUDA_TAG=12.6.2-cudnn-devel-ubuntu22.04

# Set the UV_VERSION to install
ARG UV_VERSION=0.5

# Set the Python version to install
ARG PYTHON_VERSION=3.10

#################### UV IMAGE ####################

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/cuda-python:nvidia__cuda__${CUDA_TAG}--python__${PYTHON_VERSION} AS prod

# Install uv
COPY --from=uv /uv /uvx /bin/

#################### DEV IMAGE with non-root user ################

FROM ismailbouajaja/cuda-python:nvidia__cuda__${CUDA_TAG}--python__${PYTHON_VERSION}--dev AS dev

# USER user

# Install uv
COPY --from=uv /uv /uvx /bin/

# USER root