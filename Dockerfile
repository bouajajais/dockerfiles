# syntax=docker/dockerfile:1

# Set the Poetry version to install
ARG POETRY_VERSION=1.8

# Set the Python version to install
ARG PYTHON_VERSION=3.10

# Set the Docker tag to install
ARG DOCKER_TAG=27.3.1-cli

#################### DEV IMAGE ####################

FROM ismailbouajaja/poetry:${POETRY_VERSION}--python-${PYTHON_VERSION}--dev-docker-${DOCKER_TAG} AS dev

# Change the working directory to /app/src
WORKDIR /app/src

# Copy Poetry files and install dependencies
COPY --chown=user:user ./src/pyproject.toml ./src/poetry.lock* ./

# Switch to user
USER user

# Install the dependencies
RUN poetry install --no-root

# Get the path to the Poetry virtual environment's Python executable
RUN PYTHON_PATH=$(poetry env info --executable) \
    && echo "PYTHON_PATH=${PYTHON_PATH}" >> /home/user/.python_path
USER root
RUN cat /home/user/.python_path >> /etc/environment
USER user

#################### PROD IMAGE ####################

FROM ismailbouajaja/poetry:${POETRY_VERSION}--python-${PYTHON_VERSION}--docker-${DOCKER_TAG} AS prod

# Change the working directory to /app/src
WORKDIR /app/src

# Copy Poetry files and install dependencies
COPY --chown=user:user ./src/pyproject.toml ./src/poetry.lock* ./

# Install the dependencies
RUN poetry install --no-root

# Change the working directory to /app
WORKDIR /app

# Copy the directory contents into the container at /app
COPY --chown=user:user ./ ./

# Change the working directory to /app
WORKDIR /app/src

# Set the default command for the container
CMD ["poetry", "run", "python", "main.py"]