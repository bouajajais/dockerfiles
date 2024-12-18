# syntax=docker/dockerfile:1

# Set the NODE_TAG to install
ARG NODE_TAG=16-bullseye

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/base:node__${NODE_TAG} AS prod

#################### DEV IMAGE with non-root user ################

FROM ismailbouajaja/base:node__${NODE_TAG}--dev AS dev