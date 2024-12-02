#!/bin/bash

# Run the command as the selected user
# If the command is "config" run "poetry run main.py config"
if [ "$1" = "config" ]; then
    /usr/local/bin/base-entrypoint.sh poetry run python main.py config
else
    /usr/local/bin/base-entrypoint.sh "$@"
fi