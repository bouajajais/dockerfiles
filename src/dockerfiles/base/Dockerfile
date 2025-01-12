# syntax=docker/dockerfile:1

# Set the BASE_IMAGE to install
ARG BASE_IMAGE=ubuntu:22.04

# Create a non-root user
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

#################### PROD IMAGE with non-root user ####################

FROM ${BASE_IMAGE} AS prod

# USERNAME is used as the name of the group too
ARG USERNAME
ARG USER_UID
ARG USER_GID

# Add the user and group with the specified UID/GID/USERNAME
RUN getent group ${USER_GID} || groupadd --gid ${USER_GID} ${USERNAME} \
    && getent passwd ${USER_UID} || useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}

# In case the existing user has a different username
# Update the username and group name
RUN usermod -l ${USERNAME} -d /home/${USERNAME} -m $(id -nu ${USER_UID}) \
    && groupmod -n ${USERNAME} $(id -ng ${USER_GID})

# Set the CONTAINER_USERNAME environment variable
RUN export CONTAINER_USERNAME=$(id -nu ${USER_UID}) \
    && echo >> /etc/environment \
    && echo "CONTAINER_USERNAME=$CONTAINER_USERNAME" | tee -a /etc/environment

# Install gosu
RUN apt-get update \
    && apt-get install -y gosu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY debian-entrypoint.sh /usr/local/bin/base-entrypoint.sh
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

#################### PROD IMAGE with non-root user ####################

FROM ${BASE_IMAGE} AS alpine-prod

# USERNAME is used as the name of the group too
ARG USERNAME
ARG USER_UID
ARG USER_GID

# Add the user and group with the specified UID/GID/USERNAME
RUN getent group ${USER_GID} || addgroup -g ${USER_GID} ${USERNAME} \
    && getent passwd ${USER_UID} || adduser -D -u ${USER_UID} -G ${USERNAME} -h /home/${USERNAME} -s /bin/sh ${USERNAME}

# Install su-exec and sudo and shadow
RUN apk update \
    && apk add --no-cache su-exec sudo shadow \
    # Configure passwordless sudo for the user
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# In case the existing user has a different username
# Update the username and group name
RUN usermod -l ${USERNAME} -d /home/${USERNAME} -m $(awk -F: "\$3 == ${USER_UID} {print \$1}" /etc/passwd) \
    && groupmod -n ${USERNAME} $(awk -F: "\$3 == ${USER_GID} {print \$1}" /etc/group)

# Set the CONTAINER_USERNAME environment variable
RUN export CONTAINER_USERNAME=$(awk -F: "\$3 == ${USER_UID} {print \$1}" /etc/passwd) \
    && echo "export CONTAINER_USERNAME=$CONTAINER_USERNAME" > /etc/profile.d/container_username.sh \
    && chmod 644 /etc/profile.d/container_username.sh

COPY alpine-entrypoint.sh /usr/local/bin/base-entrypoint.sh
RUN chmod +x /usr/local/bin/base-entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/base-entrypoint.sh" ]

CMD [ "sh" ]

#################### DEV IMAGE with non-root user ################

FROM alpine-prod AS alpine-dev

# Install git
RUN apk update \
    && apk add --no-cache git