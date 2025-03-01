#!/bin/bash

PROJECT_DIR=$(pwd)

function check_command {
    if ! command -v "$1" &> /dev/null
    then
        echo "$1 is not installed."
        exit 1
    fi
}

check_command "mypy"
check_command "pylint"
check_command "flake8"


echo "Starting mypy"
mypy $PROJECT_DIR

echo "Starting flake8"
flake8 $PROJECT_DIR

echo "Starting pylint"
pylint $PROJECT_DIR

echo "Done"
