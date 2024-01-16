#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: $0 <file_path or directory>"
	exit 1
fi

file_path="$1"

# Check if the file or directory exists
if [ ! -e "$file_path" ]; then
	echo "File or directory does not exist: $file_path"
	exit 1
fi

# Check if it's a directory
if [ -d "$file_path" ]; then
	# Recursively process all Python files in the directory
	find "$file_path" -type f -name "*.py" -exec sh -c '
        for file do
            echo "Processing $file..."
            autoflake --remove-all-unused-imports --in-place "$file"
            isort "$file"
            black -l 120 "$file"
        done' sh {} +
else
	# It's a single file, process it
	echo "Processing $file_path..."
	autoflake --remove-all-unused-imports --in-place "$file_path"
	isort "$file_path"
	black -l 120 "$file_path"
fi
