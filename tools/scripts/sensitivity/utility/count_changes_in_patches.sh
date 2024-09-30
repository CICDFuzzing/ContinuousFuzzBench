#!/bin/bash

# Check if at least two arguments are provided
if [ $# -lt 2 ]; then
  echo "Usage: $0 output_directory patch_directory1 [...]"
  exit 1
fi

# Create the output directory 
output_directory="$1"
mkdir -p "$output_directory"

# Shift the arguments to the next so that we can use $@ in the loop
shift  
# Loop through each patch directory 
for patch_directory in "$@"; do

  # Check if the patch directory exists
  if [ ! -d "$patch_directory" ]; then
    echo "Patch directory $patch_directory does not exist."
    continue
  fi
  
  # Extract directory name for the CSV filename
  dir_name=$(echo "$patch_directory" | awk -F'/' '{print $(NF-2)}' | cut -d'_' -f1)
  output_csv="$output_directory/${dir_name}_patches.csv"

  # Create the header
  echo "Patch,Added,Deleted,Total" > "$output_csv"

  # Process each patch file
  for patchfile in "$patch_directory"/*.patch; do

    # Check if there are any patch files
    if [ ! -e "$patchfile" ]; then
      echo "No patch files found in $patch_directory."
      continue
    fi
    
    # Get the number of added lines (starting with + but not ++)
    added_lines=$(grep -c '^[+][^+]' "$patchfile")
    # Get the number of deleted lines (starting with - but not --)
    deleted_lines=$(grep -c '^-[^-]' "$patchfile")
    # Calculate the total
    total_changes=$((added_lines + deleted_lines))

    # Store the results
    echo "$(basename "$patchfile"),$added_lines,$deleted_lines,$total_changes" >> "$output_csv"
  done

  echo "Results saved to $output_csv."
done
