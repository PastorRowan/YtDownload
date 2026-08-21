
#!/usr/bin/env bash

# run using command "source activate_venv.sh"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PARENT_DIR="$SCRIPT_DIR/.."

source "$SCRIPT_PARENT_DIR/venv/bin/activate"
