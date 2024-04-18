#!/bin/bash

# Loops on all images of current folder
for file in *; do
    # Check if the file is an image by checking the extension
    if [[ "$file" == *".jpg" || "$file" == *".jpeg" || "$file" == *".png" ]]; then
        # Gets file size
        filesize=$(stat -c %s "$file")

        # 1 Mo is 1048576 octets
        if [ $filesize -gt 1048576 ]; then
            # Rename the initial image by adding _big at the end
            mv "$file" "${file%.*}_big.${file##*.}"

            # Reduce the image size it will be 20% of the initial image file
            convert "${file%.*}_big.${file##*.}" -resize 20% "$file"
        fi
    fi
done
