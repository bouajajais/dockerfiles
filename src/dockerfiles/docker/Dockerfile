# syntax=docker/dockerfile:1

# Set the DOCKER_TAG to install
ARG DOCKER_TAG=27.3.1-cli

# Create a non-root user
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

#################### PROD IMAGE with non-root user ####################

FROM docker:${DOCKER_TAG} AS prod

ARG USERNAME
ARG USER_UID
ARG USER_GID

# Create the user and group
RUN addgroup -g ${USER_GID} ${USERNAME} \
    && adduser -u ${USER_UID} -G ${USERNAME} -h /home/${USERNAME} -s /bin/sh -D ${USERNAME}

# Install su-exec and sudo and configure passwordless sudo for the user
RUN apk update \
    && apk add --no-cache su-exec sudo \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

COPY entrypoint.sh /usr/local/bin/base-entrypoint.sh
RUN chmod +x /usr/local/bin/base-entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/base-entrypoint.sh" ]

CMD [ "sh" ]

#################### DEV IMAGE with non-root user ################

FROM prod AS dev

# Install git
RUN apk update \
    && apk add --no-cache git