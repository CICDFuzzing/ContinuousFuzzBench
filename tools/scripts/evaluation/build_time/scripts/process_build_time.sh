#!/bin/bash

# ./process_build_time.sh scratch-dir/log/build_time scratch-dir/log-data
# Sanity check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <log_dir> <output_dir>"
    exit 1
fi

log_dir="$1"
output_dir="$2"

mkdir -p $output_dir

# Loop over all log files in the directory
for file in $log_dir/*/*/*/*build.log; do
  # Extract the time using the grep and sed command
  log_name=$(basename $file)
  fuzzer_name="${log_name%%_*}"
  # Clear or create the output file
  if [[ ! -f $output_dir/"$fuzzer_name"_build_time ]]; then 
      echo "benchmark,time,file_name" > $output_dir/"$fuzzer_name"_build_time
  fi
  time=$(grep -B 2 'exporting to image' "$file" | grep 'DONE' | sed -n 's/.*DONE \([0-9.]*s\).*/\1/p')
  # Check if time is found and write to CSV
  if [ -n "$time" ]; then
    file_name=$(echo $file | rev | cut -d'/' -f1-3 | rev)
    benchmark_name=$(basename $file_name | awk -F'_' '{print $2"_"$3"_"$4}')
    echo "$benchmark_name,$time,$file_name" >> $output_dir/"$fuzzer_name"_build_time
  fi
done
