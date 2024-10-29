#!/bin/bash -e
shopt -s extglob

# Sanity check
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <results>"
    exit 1
fi
dir_path=$1

output_path="./log/temp_stats"

for log_path in "$dir_path"/*/*/*/
do
    echo $log_path
    find "$log_path" -type f -name "fuzzer_stats" | while read stats_file; 
    do
        #echo $stats_file
        fuzzer_name=$(echo $stats_file | awk -F'/' '{print $(NF-6)}')
        #echo "$fuzzer_name"
        target_name=$(echo $stats_file | awk -F'/' '{print $(NF-5)}')
        #echo "$target_name"
        program_name=$(echo $stats_file | awk -F'/' '{print $(NF-4)}')
        #echo "$program_name"
        iter_num=$(echo $stats_file | awk -F'/' '{print $(NF-3)}')
        findings_path=$(echo $stats_file | rev | cut -d'/' -f2- | rev)
        if [[ -n "$stats_file" ]]; then 
            stats="$fuzzer_name,$target_name,$program_name,$iter_num,$(awk '/start_time/ || /last_update/ || /execs_done/ || /unique_crashes/' $stats_file | cut -c 21- | paste -s -d, -)" 
        else 
            stats="$fuzzer_name,$target_name,$program_name,$iter_num"
        fi 
        mkdir -p "$output_path/$fuzzer_name"
        echo "$stats" >> "$output_path/$fuzzer_name/$fuzzer_name"_"$target_name"_"$program_name"_fuzzer_stats
    done 
done
