# syntax=docker/dockerfile:1

# Set the CUDA version to install
ARG CUDA_TAG=12.6.2-cudnn-devel-ubuntu22.04

#################### BASE IMAGE with non-root user ####################

FROM ismailbouajaja/base:cuda-${CUDA_TAG} AS base

#################### DEV BASE IMAGE with non-root user ################

FROM ismailbouajaja/base:dev-cuda-${CUDA_TAG} AS dev-base