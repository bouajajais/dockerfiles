# syntax=docker/dockerfile:1

# Set the BASE_IMAGE to install
ARG BASE_IMAGE=ubuntu:22.04

# Create a non-root user
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

#################### PROD IMAGE with non-root user ####################

FROM ${BASE_IMAGE} AS prod

ARG USERNAME
ARG USER_UID
ARG USER_GID

# Create the user and group with the specified UID/GID
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
    && apt-get update \
    && apt-get install -y gosu

COPY entrypoint.sh /usr/local/bin/base-entrypoint.sh
RUN chmod +x /usr/local/bin/base-entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/base-entrypoint.sh" ]

CMD [ "sh" ]

#################### DEV IMAGE with non-root user ################

FROM prod AS dev

ARG USERNAME

# Install git and sudo and configure passwordless sudo for the user
RUN apt-get update \
    && apt-get install -y git sudo \
    && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}