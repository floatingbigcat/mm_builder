#!/bin/bash

# Specify the folder path
folder_path="your_dump_path"

# Iterate over each file in the folder
for file in "$folder_path"/*.bz2; do
    # Check if the file is a regular file (not a directory)
    if [ -f "$file" ]; then
        # Display the file name
        echo "Unzipping $file..."&
        
        # Unzip the file
        bzip2 -d "$file"&
        
        # Remove the .bz2 extension from the file name
        unzipped_file="${file%.bz2}"&
        
        # Display the unzipped file name
        echo "Unzipped file: $unzipped_file"&
    fi
done
