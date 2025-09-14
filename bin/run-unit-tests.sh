#!/bin/bash

set -e

BASEDIR="` dirname $( dirname $( realpath $0 ) ) `"

source "$BASEDIR/env/bin/activate"

PY_SCRIPT="$BASEDIR/bin/run-unit-tests.py"

"$BASEDIR/env/bin/python3" $PY_SCRIPT $1
 


