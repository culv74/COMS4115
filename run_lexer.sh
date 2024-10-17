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

# Check if a file is provided as an argument
if [ "$#" -eq 1 ]; then
    input_file=$1
    if [ -f "$input_file" ]; then
        # Run the lexer with the provided input file
        python3 lexer.py "$input_file"
    else
        echo "Error: File '$input_file' not found."
        exit 1
    fi
else
    # Prompt the user to enter code to be tokenized
    echo "Enter the code to be tokenized (end with EOF/Ctrl+D):"
    input_code=$(cat)
    
    # Run the lexer with the input code
    python3 lexer.py --input "$input_code"
fi
