#!/bin/bash -e

# Sanity check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <output_path> <coverage_path>"
    exit 1
fi

output_path=$1
coverage_path=$2

export experiment=$(echo $coverage_path | cut -d '/' -f7)

mkdir -p $output_path

for log_path in "$coverage_path"/ar/*/*/*/*/coverage/*total_coverage.txt
do  
    # echo $log_path
    export target_name=$(echo $log_path | cut -d '/' -f10)
    export program_name=$(echo $log_path | cut -d '/' -f11)

    if [[ ! -f "$output_path/$experiment"_total_coverage ]]; then 
        header=$(head -n 1 "$log_path" | sed -r 's/\s+/,/g')
        echo "TARGET,PROGRAM,$header" > "$output_path/$experiment"_total_coverage
    fi
    output=$(tail -n 1 "$log_path" | sed -r 's/\s+/,/g')
    echo "$target_name,$program_name,$output"
    echo "$target_name,$program_name,$output" >> "$output_path/$experiment"_total_coverage
done;
