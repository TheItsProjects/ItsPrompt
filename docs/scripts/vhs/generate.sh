#!/bin/bash

# Run this file to create tapes for all .tape files in the directory.
# The tapes will be saved to source/media.
# To run this file, you need to have vhs installed. Read more in the development guide.

trap "echo 'Script interrupted by user'; exit 1" SIGINT SIGTERM

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Iterate over all .tape files in the directory
for file in "$DIR"/*.tape
do
  # Run the file with vhs
  echo "--- Creating media for $file ---"
  vhs "$file" 1> /dev/null
done
