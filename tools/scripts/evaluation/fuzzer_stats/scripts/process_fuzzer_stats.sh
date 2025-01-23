#!/bin/bash -e
shopt -s extglob

# ./process_fuzzer_stats.sh scratch-dir/log-data/aflgoexp scratch-dir/log/fuzzer_stats
# Sanity check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <log_dir> <output_dir>"
    exit 1
fi

log_dir="$1"
output_dir="$2"

mkdir -p $output_dir

for log_path in "$log_dir"/*/*/*/
do
    echo $log_path
    find "$log_path" -type f -name "fuzzer_stats" | while read stats_file; 
    do
        echo $stats_file
        fuzzer_name=$(echo $stats_file | awk -F'/' '{print $(NF-5)}')
        echo "$fuzzer_name"
        target_name=$(echo $stats_file | awk -F'/' '{print $(NF-4)}')
        echo "$target_name"
        program_name=$(echo $stats_file | awk -F'/' '{print $(NF-3)}')
        echo "$program_name"
        iter_num=$(echo $stats_file | awk -F'/' '{print $(NF-2)}')
        findings_path=$(echo $stats_file | rev | cut -d'/' -f2- | rev)
        if [[ -n "$stats_file" ]]; then 
            stats="$fuzzer_name,$target_name,$program_name,$iter_num,$(awk '/start_time/ || /last_update/ || /execs_done/ || /unique_crashes/' $stats_file | cut -c 21- | paste -s -d, -)" 
        else 
            stats="$fuzzer_name,$target_name,$program_name,$iter_num"
        fi 
        mkdir -p "$output_dir/$fuzzer_name"
        echo "$stats" >> "$output_dir/$fuzzer_name/$fuzzer_name"_"$target_name"_"$program_name"_fuzzer_stats
    done 
done
