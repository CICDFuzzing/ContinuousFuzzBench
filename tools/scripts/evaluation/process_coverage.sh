#!/bin/bash -e

# Sanity check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <output_path> <coverage_path>"
    exit 1
fi

output_path=$1
coverage_path=$2

mkdir -p $output_path

if [[ "$coverage_path" == *"aflgo"* ]]; then
    export experiment=$(echo $coverage_path | cut -d '/' -f9)
    echo $experiment
    for log_path in "$coverage_path"/ar/*/*/*/*/coverage/*target_file_coverage.txt
    do  
        echo $log_path
        export target_name=$(echo $log_path | cut -d '/' -f12)
        export program_name=$(echo $log_path | cut -d '/' -f13)
        export iter_num=$(basename $log_path | sed -n 's/.*_\(.*\)_target_file_coverage.*/\1/p')
        if [[ ! -f "$output_path/$experiment"_"$target_name"_"$program_name"_target_file_coverage ]]; then 
            header=$(head -n 1 "$log_path" | sed -r 's/\s+/,/g')
            echo "TARGET,PROGRAM,ITER,Filename,Regions,Missed_Regions,Cover,Functions,Missed_Functions,Executed,Lines,Missed_Lines,Cover,Branches,Missed_Branches,Cover" > "$output_path/$experiment"_"$target_name"_"$program_name"_target_file_coverage
        fi
        output=$(tail -n 1 "$log_path" | sed -r 's/\s+/,/g')

        echo "$target_name,$program_name,$iter_num,$output"
        echo "$target_name,$program_name,$iter_num,$output" >> "$output_path/$experiment"_"$target_name"_"$program_name"_target_file_coverage
    done;
fi
