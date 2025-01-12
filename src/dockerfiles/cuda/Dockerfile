# syntax=docker/dockerfile:1

# Set the CUDA version to install
ARG CUDA_TAG=12.6.2-cudnn-devel-ubuntu22.04

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/base:nvidia__cuda__${CUDA_TAG} AS prod

USER user
RUN echo "PATH=\"/usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}\"" > /home/user/temp-environment
USER root
RUN cat /home/user/temp-environment >> /etc/environment

COPY ./cuda-entrypoint.sh /usr/local/bin/cuda-entrypoint.sh
RUN chmod +x /usr/local/bin/cuda-entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/cuda-entrypoint.sh" ]

#################### DEV IMAGE with non-root user ################

FROM ismailbouajaja/base:nvidia__cuda__${CUDA_TAG}--dev AS dev

USER user
RUN echo "PATH=\"/usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}\"" > /home/user/temp-environment
USER root
RUN cat /home/user/temp-environment >> /etc/environment

COPY ./cuda-entrypoint.sh /usr/local/bin/cuda-entrypoint.sh
RUN chmod +x /usr/local/bin/cuda-entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/cuda-entrypoint.sh" ]