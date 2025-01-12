# syntax=docker/dockerfile:1

# Set the NODE_TAG to install
ARG NODE_TAG=22-bullseye-slim

# mkdir myproject
# docker run --rm -v ./myproject:/app/myproject ismailbouajaja/create-react-router

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/node:node__${NODE_TAG}--dev AS prod

# Install the create-react-router package globally
RUN npm install -g create-react-router@latest

WORKDIR /app

# Install the dependencies
CMD ["sh", "-c", "cd */ && npx create-react-router@latest . --install --no-git-init"]

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/node:node__${NODE_TAG}--alpine-dev AS alpine-prod

# Install the create-react-router package globally
RUN npm install -g create-react-router@latest

WORKDIR /app

# Install the dependencies
CMD ["sh", "-c", "cd */ && npx create-react-router@latest . --install --no-git-init"]