#!/bin/bash

set -e

# Activate virtual environment.
. /venv/bin/activate

# Exececute the container's main process;
# i.e., what's set as CMD in the Dockerfile.
exec "$@"
