#!/bin/bash -e

# Sanity check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <output_path> <log_dir>"
    exit 1
fi

output_path="$1"
log_dir="$2"

output_file="results.csv"
> "$output_path"/"$output_file"

for file in "$log_dir"/*_build.log; do
    func_name=$(grep -A 1 'Function targets' "$file" | tail -n 1 | awk '{print $3}')
    file_name=$(basename $file)
    echo "$func_name,$file_name" >> "$output_path"/"$output_file"
done
