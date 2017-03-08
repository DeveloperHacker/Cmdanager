#!/usr/bin/env bash

SRC="src"
TEST="${SRC}/tests"
export PYTHONPATH="${PYTHONPATH}:${SRC}"

clear
echo "============================== test10.py =============================="
python3 "${TEST}/test10.py"
