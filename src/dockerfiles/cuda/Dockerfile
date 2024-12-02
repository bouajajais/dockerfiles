# syntax=docker/dockerfile:1

# Set the CUDA version to install
ARG CUDA_TAG=12.6.2-cudnn-devel-ubuntu22.04

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/base:nvidia__cuda__${CUDA_TAG} AS prod

#################### DEV IMAGE with non-root user ################

FROM ismailbouajaja/base:nvidia__cuda__${CUDA_TAG}--dev AS dev