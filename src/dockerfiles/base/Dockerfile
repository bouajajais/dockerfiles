# syntax=docker/dockerfile:1

# Set the BASE_IMAGE to install
ARG BASE_IMAGE=ubuntu:22.04

# Create a non-root user
ARG DEFAULT_USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

#################### PROD IMAGE with non-root user ####################

FROM ${BASE_IMAGE} AS prod

ARG DEFAULT_USERNAME
ARG USER_UID
ARG USER_GID

# Create the user and group with the specified UID/GID/DEFAULT_USERNAME
RUN getent group ${USER_GID} || groupadd --gid ${USER_GID} ${DEFAULT_USERNAME} \
    && getent passwd ${USER_UID} || useradd --uid ${USER_UID} --gid ${USER_GID} -m ${DEFAULT_USERNAME} \
    && apt-get update \
    && apt-get install -y gosu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Set the CONTAINER_USERNAME environment variable
    && export CONTAINER_USERNAME=$(id -nu ${USER_UID}) \
    && echo >> /etc/environment \
    && echo "CONTAINER_USERNAME=$CONTAINER_USERNAME" | tee -a /etc/environment

COPY entrypoint.sh /usr/local/bin/base-entrypoint.sh
RUN chmod +x /usr/local/bin/base-entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/base-entrypoint.sh" ]

CMD [ "sh" ]

#################### DEV IMAGE with non-root user ################

FROM prod AS dev

# Install git and sudo and configure passwordless sudo for the user
RUN . /etc/environment \
    && apt-get update \
    && apt-get install -y git sudo \
    && echo ${CONTAINER_USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${CONTAINER_USERNAME} \
    && chmod 0440 /etc/sudoers.d/${CONTAINER_USERNAME}