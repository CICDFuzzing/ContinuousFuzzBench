#!/bin/bash -e
shopt -s extglob

# Sanity check
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <results>"
    exit 1
fi
dir_path=$1

export output_path="./log"

for log_path in "$dir_path"/*/*/*/
do
    echo $log_path
    export experiment=$(echo $log_path | cut -d'/' -f7)
    mkdir -p $output_path/$experiment
    # the target and program names
    export info=$(echo $log_path | cut -d'/' -f9- | tr / ,)
    echo "Processing $experiment..."
    find "$log_path" -type f -name "fuzzer_stats" | while read stats_file; 
    do
        echo $stats_file
        export findings_path=$(echo $stats_file | rev | cut -d'/' -f2- | rev)
        export iteration=$(echo $stats_file | rev | cut -d'/' -f 4 |rev)
        if [[ -n "$stats_file" ]]; then 
            export stats="$info$(awk '/start_time/ || /last_update/ || /execs_done/ || /execs_per_sec/ || /unique_crashes/ || /execs_since_crash/' $stats_file | cut -c 21- | paste -s -d, -)" 
        else 
            export stats="$info"
        fi 
        echo "$stats,$findings_path" >> "$output_path/$experiment/$experiment"_"$iteration"_filtered_fuzzer_stats
    done 
done
