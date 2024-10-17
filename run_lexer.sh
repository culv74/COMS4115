#!/bin/bash

# Install Python3 if it is not installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Installing Python3..."
    if [ "$(uname)" == "Linux" ]; then
        sudo apt update && sudo apt install -y python3
    elif [ "$(uname)" == "Darwin" ]; then
        brew install python3
    else
        echo "Unsupported OS. Please install Python3 manually."
        exit 1
    fi
fi

# Prompt the user to enter code to be tokenized
echo "Enter the code to be tokenized (end with EOF/Ctrl+D):"
input_code=$(cat)

# Run the lexer with the input code
python3 lexer.py --input "$input_code"
