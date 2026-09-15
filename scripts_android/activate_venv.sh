
#!/usr/bin/env bash

# Activate this script using:
# source activate_venv.sh
#
# The script must be sourced rather than executed normally so that the
# virtual environment's environment changes are applied to the current
# shell session.

# Determine the absolute path of the directory containing this script.
# This allows the script to locate the project's virtual environment
# regardless of the directory from which the script is run.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# The script is located in the scripts_android directory, so its parent
# directory is the YtDownload project root.
SCRIPT_PARENT_DIR="$SCRIPT_DIR/.."

# Activate the Python virtual environment located in the project root.
# This makes the project's isolated Python interpreter and installed
# packages available in the current shell session.
source "$SCRIPT_PARENT_DIR/venv/bin/activate"
