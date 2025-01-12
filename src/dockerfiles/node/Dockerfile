# syntax=docker/dockerfile:1

# Set the NODE_TAG to install
ARG NODE_TAG=22-bullseye-slim

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/base:node__${NODE_TAG} AS prod

#################### DEV IMAGE with non-root user ################

FROM ismailbouajaja/base:node__${NODE_TAG}--dev AS dev

#################### ALPINE-PROD IMAGE with non-root user ####################

FROM ismailbouajaja/base:node__${NODE_TAG}--alpine-prod AS alpine-prod

#################### ALPINE-DEV IMAGE with non-root user ################

FROM ismailbouajaja/base:node__${NODE_TAG}--alpine-dev AS alpine-dev