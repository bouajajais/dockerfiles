ENV_FILE="${1:-.user_guid.env}"
USER_UID="${2:-$(id -u)}"
USER_GID="${3:-$(id -g)}"

# Check if ${ENV_FILE} exists
if [ ! -f ${ENV_FILE} ]; then
    # Create ${ENV_FILE} and add the variables
    echo "USER_UID=${USER_UID}" > ${ENV_FILE}
    echo "USER_GID=${USER_GID}" >> ${ENV_FILE}
else
    # Check if USER_UID is already defined
    if grep -q "^USER_UID=" ${ENV_FILE}; then
        sed -i "s/^USER_UID=.*/USER_UID=${USER_UID}/" ${ENV_FILE}
    else
        # Add a new line at the end of the file if it doesn't already end with a newline
        if ! tail -c 1 ${ENV_FILE} | grep -q '^$'; then
            echo >> ${ENV_FILE}
        fi
        echo "USER_UID=${USER_UID}" >> ${ENV_FILE}
    fi

    # Check if USER_GID is already defined
    if grep -q "^USER_GID=" ${ENV_FILE}; then
        sed -i "s/^USER_GID=.*/USER_GID=${USER_GID}/" ${ENV_FILE}
    else
        # Add a new line at the end of the file if it doesn't already end with a newline
        if ! tail -c 1 ${ENV_FILE} | grep -q '^$'; then
            echo >> ${ENV_FILE}
        fi
        echo "USER_GID=${USER_GID}" >> ${ENV_FILE}
    fi
fi