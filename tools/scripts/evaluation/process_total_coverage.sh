#!/bin/bash -e

# Sanity check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <output_path> <coverage_path>"
    exit 1
fi

output_path=$1
coverage_path=$2

mkdir -p $output_path
experiment=$(echo $coverage_path | cut -d '/' -f7)
echo $experiment
for log_path in "$coverage_path"/ar/*/*/*/*/coverage/*total_coverage.txt
do  
    echo $log_path
    fuzzer_name=$(basename $log_path | cut -d'_' -f1)
    target_name=$(echo $log_path | cut -d '/' -f10)
    program_name=$(echo $log_path | cut -d '/' -f11)
    iter_num=$(basename $log_path | sed -n 's/.*_\(.*\)_total_coverage.*/\1/p')

    # echo $fuzzer_name
    # echo $target_name
    # echo $program_name
    # echo $iter_num
    mkdir -p $output_path/$fuzzer_name
    if [[ ! -f "$output_path/$fuzzer_name/$fuzzer_name"_"$target_name"_"$program_name"_total_coverage ]]; then 
        header=$(head -n 1 "$log_path" | sed -r 's/\s+/,/g')
        echo "TARGET,PROGRAM,ITER,Filename,Regions,Missed_Regions,Cover,Functions,Missed_Functions,Executed,Lines,Missed_Lines,Cover,Branches,Missed_Branches,Cover" > "$output_path/$fuzzer_name/$fuzzer_name"_"$target_name"_"$program_name"_total_coverage
    fi
    output=$(tail -n 1 "$log_path" | sed -r 's/\s+/,/g')
    #echo "$target_name,$program_name,$iter_num,$output"
    echo "$target_name,$program_name,$iter_num,$output" >> "$output_path/$fuzzer_name/$fuzzer_name"_"$target_name"_"$program_name"_total_coverage
done;
