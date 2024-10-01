#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: $0 <directory> <num_patches>"
  exit 1
fi

directory="$1"
num_patches="$2"

for file in "$directory"/*; do
  echo "For $file"
  if [[ -f "$file" ]]; then
    # Randomly select n patches
    selected_patches=$(shuf -n "$num_patches" "$file")
    echo "selected patches:"
    echo "$selected_patches"

    # for patch_url in $selected_patches; do
    #   curl -O "$patch_url"
    # done
  fi
done
