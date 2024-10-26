#!/bin/bash

# Sanity check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <output_path> <log_dir>"
    exit 1
fi

output_file="$1"
log_dir="$2"

echo "time,file_name" > "$output_file"

for file in $log_dir/*.log; do

  time=$(grep -B 2 'exporting to image' "$file" | grep 'DONE' | sed -n 's/.*DONE \([0-9.]*s\).*/\1/p')
  
  if [ -n "$time" ]; then
    file_name=$(echo $file | rev | cut -d'/' -f1-3 | rev)
    echo "$time,$file_name" >> "$output_file"
  fi
done
