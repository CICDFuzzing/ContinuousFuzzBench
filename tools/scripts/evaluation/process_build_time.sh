#!/bin/bash

# Sanity check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <output_path> <log_dir>"
    exit 1
fi

# Output CSV file
output_file="$1"
log_dir="$2"

# Clear or create the output file
echo "time,file_name" > "$output_file"

# Loop over all log files in the directory
for file in $log_dir/*.log; do
  # Extract the time using the grep and sed command
  time=$(grep -B 2 'exporting to image' "$file" | grep 'DONE' | sed -n 's/.*DONE \([0-9.]*s\).*/\1/p')
  
  # Check if time is found and write to CSV
  if [ -n "$time" ]; then
    file_name=$(echo $file | rev | cut -d'/' -f1-3 | rev)
    echo "$time,$file_name" >> "$output_file"
  fi
done
