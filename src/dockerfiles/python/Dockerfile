# syntax=docker/dockerfile:1

# Set the PYTHON_TAG to install
ARG PYTHON_TAG=3.10-slim

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/base:python__${PYTHON_TAG} AS prod

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

#################### DEV IMAGE with non-root user ################

FROM ismailbouajaja/base:python__${PYTHON_TAG}--dev AS dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1