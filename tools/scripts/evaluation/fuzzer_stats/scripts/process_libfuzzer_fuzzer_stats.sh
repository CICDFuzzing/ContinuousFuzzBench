#!/bin/bash -e

# ./process_libfuzzer_fuzzer_stats.sh scratch-dir/log-data/libfuzzer scratch-dir/log/fuzzer_stats/libfuzzer
# Sanity check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <log_dir> <output_dir>"
    exit 1
fi

log_dir="$1"
output_dir="$2"

mkdir -p $output_dir

# Loop over all log files in the directory
for file in $log_dir/*/*/*container.log; do
  # Extract the time using the grep and sed command
  log_name=$(basename $file)
  fuzzer_name=$(echo $log_name | awk -F'_' '{print $1}')
  benchmark_name=$(echo $log_name | awk -F'_' '{print $2"_"$3"_"$4}')
  iter_num=$(echo $log_name | sed -E 's/.*_([0-9]+)_container\.log/\1/')
  echo $file
  echo $log_name
  echo $fuzzer_name
  echo $benchmark_name
  echo $iter_num
  # Clear or create the output file
  mkdir -p "$output_dir/$fuzzer_name"
  result_path="${output_dir}/${fuzzer_name}/${fuzzer_name}_${benchmark_name}_fuzzer_stats"
  if [[ ! -f "$result_path" ]]; then 
      echo "FUZZER,TARGET,ITER,runtime,execs_done,unique_crashes,oom,timeout" > "$result_path"
  fi
  output=$(awk '/^#/{line=$0} /libFuzzer: run interrupted; exiting/{print line; exit}' "$file" | awk -F'[: ]+' '{split($(NF-6), crash, "/"); sub(/s$/, "", $(NF-4)); sub(/^#/, "", $(NF-16)); print $(NF-4) "," $(NF-16) "," crash[3] "," crash[1] "," crash[2]}')
  # Check if time is found and write to CSV
  if [ -n "$output" ]; then
    echo "$fuzzer_name,$benchmark_name,$iter_num,$output" >> "$result_path"
  fi
done
