#!/bin/sh

# This script is used to change the UID and GID of the user running the container
# to match the UID and GID of the user on the host machine. This is done to avoid
# permission issues when mounting volumes from the host machine to the container.
# This script must be run as the root user.

USERNAME=user

# Exit if not connected as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Define the USER_UID and USER_GID environment variables instead."
    exit 1
fi

# Exit if /var/run/docker.sock does not exist
if [ ! -S /var/run/docker.sock ]; then
    echo "The Docker socket file /var/run/docker.sock was not found."
    echo "Make sure to mount the Docker socket file to the container using -v /var/run/docker.sock:/var/run/docker.sock"
    exit 1
fi

# Warn the user if the USER_UID and USER_GID environment variables are not provided
# and use the default UID and GID if not provided
if [ -z "${USER_UID}" ] || [ -z "${USER_GID}" ]; then
    echo "WARNING: Docker container was run without USER_UID and USER_GID environment variables."
    echo "The container will run with the default UID and GID of the ${USERNAME}:$(id -u ${USERNAME}):$(id -g ${USERNAME}) user."
    USER_UID=$(id -u ${USERNAME})
    USER_GID=$(id -g ${USERNAME})
fi

# Warn the user if the WORKDIR environment variable is not provided
if [ -z "${WORKDIR}" ]; then
    echo "WARNING: Docker container was run without WORKDIR environment variable."
    echo "Only /home/${USERNAME} ownership will be changed to the selected UID and GID."
fi

# Check if the selected user does NOT correspond to the default user
if [ "$(id -u ${USERNAME})" -ne "${USER_UID}" ] || [ "$(id -g ${USERNAME})" -ne "${USER_GID}" ]; then
    # Change ownership of the home directory
    chown -R ${USER_UID}:${USER_GID} /home/${USERNAME}

    if [ -n "${WORKDIR}" ]; then
        # Change ownership of application directory
        chown -R ${USER_UID}:${USER_GID} ${WORKDIR}
    fi

    # Change the GID of the user group if it is different
    if [ "$(id -g ${USERNAME})" -ne "${USER_GID}" ]; then
        delgroup ${USERNAME}
        addgroup -g ${USER_GID} ${USERNAME}
    fi

    # Change the UID of the user if it is different
    if [ "$(id -u ${USERNAME})" -ne "${USER_UID}" ]; then
        deluser ${USERNAME}
        adduser -u ${USER_UID} -G ${USERNAME} -h /home/${USERNAME} -s /bin/sh -D ${USERNAME}
    fi
fi

# Run the command as the selected user
exec su-exec ${USERNAME} "$@"