#!/bin/sh

## This script is used to change the UID and GID of the user running the container
## to match the UID and GID of the user on the host machine. This is done to avoid
## permission issues when mounting volumes from the host machine to the container.
## This script must be run as the root user.

# Default value for VERBOSE_ENTRYPOINT to 1
VERBOSE_ENTRYPOINT=${VERBOSE_ENTRYPOINT:-1}

# Get CONTAINER_USERNAME from /etc/environment
. /etc/environment

# Exit if not connected as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Define the USER_UID and USER_GID environment variables instead."
    exit 1
fi

# Warn the user if the USER_UID and USER_GID environment variables are not provided
# and use the default UID and GID if not provided
if [ -z "${USER_UID}" ] || [ -z "${USER_GID}" ]; then
    if [ "${VERBOSE_ENTRYPOINT}" -ne 0 ]; then
        echo "WARNING: Docker container was run without USER_UID and USER_GID environment variables."
        echo "The container will run with the default UID and GID of the ${CONTAINER_USERNAME}:$(id -u ${CONTAINER_USERNAME}):$(id -g ${CONTAINER_USERNAME}) user."
    fi
    USER_UID=$(id -u ${CONTAINER_USERNAME})
    USER_GID=$(id -g ${CONTAINER_USERNAME})
fi

# Change the GID of the user group if it is different
if [ "$(id -g ${CONTAINER_USERNAME})" -ne "${USER_GID}" ]; then
    # Change ownership of files and directories owned by the default user
    if [ "${VERBOSE_ENTRYPOINT}" -ne 0 ]; then
        echo "Changing GID of files and directories owned by ${CONTAINER_USERNAME} to ${USER_GID}"    
        find / -group ${CONTAINER_USERNAME} -exec chgrp ${USER_GID} {} \; -print 2>/dev/null
    else
        find / -group ${CONTAINER_USERNAME} -exec chgrp ${USER_GID} {} \; 2>/dev/null
    fi

    # Change the GID of the user group
    if [ "${VERBOSE_ENTRYPOINT}" -ne 0 ]; then
        echo "Changing GID of the user group to ${USER_GID}"
    fi
    groupmod -g ${USER_GID} ${CONTAINER_USERNAME}
fi

# Change the UID of the user if it is different
if [ "$(id -u ${CONTAINER_USERNAME})" -ne "${USER_UID}" ]; then
    # Change ownership of files and directories owned by the default user
    if [ "${VERBOSE_ENTRYPOINT}" -ne 0 ]; then
        echo "Changing UID of files and directories owned by ${CONTAINER_USERNAME} to ${USER_UID}"
        find / -user ${CONTAINER_USERNAME} -exec chown ${USER_UID} {} \; -print 2>/dev/null
    else
        find / -user ${CONTAINER_USERNAME} -exec chown ${USER_UID} {} \; 2>/dev/null
    fi

    # Change the UID of the user
    if [ "${VERBOSE_ENTRYPOINT}" -ne 0 ]; then
        echo "Changing UID of the user to ${USER_UID}"
    fi
    usermod -u ${USER_UID} ${CONTAINER_USERNAME}
fi

# Run the command as the selected user
export CONTAINER_USERNAME=${CONTAINER_USERNAME}
if [ "${VERBOSE_ENTRYPOINT}" -ne 0 ]; then
    echo "Running command as ${CONTAINER_USERNAME}"
fi
exec gosu ${CONTAINER_USERNAME} "$@"