# syntax=docker/dockerfile:1

# Set the UV_TAG to install
ARG UV_TAG=3.10-slim

# docker run --rm -v .:/app ismailbouajaja/uv-init --lib libname

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/base:ghcr.io__astral-sh__uv__${UV_TAG}--dev AS prod

WORKDIR /app

# Initialize the Poetry project
ENTRYPOINT [ "/usr/local/bin/base-entrypoint.sh", "uv", "init" ]

CMD [ "." ]

#################### ALPINE-PROD IMAGE with non-root user ####################

FROM ismailbouajaja/base:ghcr.io__astral-sh__uv__${UV_TAG}--alpine-dev AS alpine-prod

WORKDIR /app

# Initialize the Poetry project
ENTRYPOINT [ "/usr/local/bin/base-entrypoint.sh", "uv", "init" ]

CMD [ "." ]