# syntax=docker/dockerfile:1

# Set the Poetry version to install
ARG POETRY_VERSION=1.8

# Set the Python version to install
ARG PYTHON_TAG=3.10-slim

# mkdir myproject
# docker run --rm -v ./myproject:/app ismailbouajaja/poetry-init

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/poetry:poetry__${POETRY_VERSION}--python__${PYTHON_TAG}--dev AS prod

WORKDIR /app

# Create a script to initialize the Poetry project interactively
ENV PATH="${PATH}:/usr/local/bin"
RUN echo "poetry init" > /usr/local/bin/it && chmod +x /usr/local/bin/it

# Set the entrypoint to run the script
ENTRYPOINT [ "/usr/local/bin/base-entrypoint.sh", "bash", "-c" ]

# Initialize the Poetry project
CMD [ "poetry init --no-interaction" ]

#################### ALPINE-PROD IMAGE with non-root user ####################

FROM ismailbouajaja/poetry:poetry__${POETRY_VERSION}--python__${PYTHON_TAG}--alpine-dev AS alpine-prod

WORKDIR /app

# Create a script to initialize the Poetry project interactively
ENV PATH="${PATH}:/usr/local/bin"
RUN echo "poetry init" > /usr/local/bin/it && chmod +x /usr/local/bin/it

# Set the entrypoint to run the script
ENTRYPOINT [ "/usr/local/bin/base-entrypoint.sh", "bash", "-c" ]

# Initialize the Poetry project
CMD [ "poetry init --no-interaction" ]