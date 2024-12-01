# syntax=docker/dockerfile:1

# Set the DOCKER_TAG to install
ARG DOCKER_TAG=27.3.1-cli

# Set the PYTHON_VERSION to install
ARG PYTHON_VERSION=3.10

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/docker:docker__${DOCKER_TAG} AS prod

ARG PYTHON_VERSION

# Install build tools and Python dependencies
RUN apk update \
    && apk add --no-cache \
    bash \
    curl \
    gcc \
    make \
    musl-dev \
    zlib-dev \
    bzip2-dev \
    xz-dev \
    readline-dev \
    libffi-dev \
    sqlite-dev \
    openssl-dev \
    gdbm-dev \
    ncurses-dev \
    linux-headers

USER user

ENV PYENV_ROOT="/home/user/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"

# Install pyenv
RUN curl https://pyenv.run | bash \
    && pyenv install ${PYTHON_VERSION} \
    && pyenv global ${PYTHON_VERSION}

RUN sudo ln -sf ~/.pyenv/versions/$(pyenv versions --bare | grep -E "^${PYTHON_VERSION}\." | tail -n 1)/bin/python${PYTHON_VERSION} /usr/bin/python3 \
    && sudo ln -sf ~/.pyenv/versions/$(pyenv versions --bare | grep -E "^${PYTHON_VERSION}\." | tail -n 1)/bin/python${PYTHON_VERSION} /usr/bin/python \
    && sudo ln -sf ~/.pyenv/versions/$(pyenv versions --bare | grep -E "^${PYTHON_VERSION}\." | tail -n 1)/bin/pip${PYTHON_VERSION} /usr/bin/pip3 \
    && sudo ln -sf ~/.pyenv/versions/$(pyenv versions --bare | grep -E "^${PYTHON_VERSION}\." | tail -n 1)/bin/pip${PYTHON_VERSION} /usr/bin/pip

USER root

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

#################### DEV IMAGE with non-root user ################

FROM ismailbouajaja/docker:docker__${DOCKER_TAG}--dev AS dev

ARG PYTHON_VERSION

# Install build tools and Python dependencies
RUN apk update \
    && apk add --no-cache \
    bash \
    curl \
    gcc \
    make \
    musl-dev \
    zlib-dev \
    bzip2-dev \
    xz-dev \
    readline-dev \
    libffi-dev \
    sqlite-dev \
    openssl-dev \
    gdbm-dev \
    ncurses-dev \
    linux-headers

USER user

ENV PYENV_ROOT="/home/user/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"

# Install pyenv
RUN curl https://pyenv.run | bash \
    && pyenv install ${PYTHON_VERSION} \
    && pyenv global ${PYTHON_VERSION}

RUN sudo ln -sf ~/.pyenv/versions/$(pyenv versions --bare | grep -E "^${PYTHON_VERSION}\." | tail -n 1)/bin/python${PYTHON_VERSION} /usr/bin/python3 \
    && sudo ln -sf ~/.pyenv/versions/$(pyenv versions --bare | grep -E "^${PYTHON_VERSION}\." | tail -n 1)/bin/python${PYTHON_VERSION} /usr/bin/python \
    && sudo ln -sf ~/.pyenv/versions/$(pyenv versions --bare | grep -E "^${PYTHON_VERSION}\." | tail -n 1)/bin/pip${PYTHON_VERSION} /usr/bin/pip3 \
    && sudo ln -sf ~/.pyenv/versions/$(pyenv versions --bare | grep -E "^${PYTHON_VERSION}\." | tail -n 1)/bin/pip${PYTHON_VERSION} /usr/bin/pip

USER root

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1