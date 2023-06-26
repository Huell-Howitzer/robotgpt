#!/bin/bash

# Find all subdirectories under /app and append them to the Python path
echo Lets set the python path
for dir in $(find /app -type d)
do
    export PYTHONPATH="${PYTHONPATH}:${dir}"
    echo Added "${dir}" to the python path
done

# Run the command passed to this script
echo PYTHONPATH="${PYTHONPATH}"
exec "$@"
