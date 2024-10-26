#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <path_to_csv_file> <path_to_log_directory> <output_path>"
    exit 1
fi

csv_file="$1"
log_dir="$2"
output_path="$3"

echo "Processing $log_dir..."

while IFS=',' read -r function_name file_name; do

    base_name=$(basename "$file_name" .log)  
    base_name=${base_name%_*}                 
    base_name=${base_name#*_}                 

    if [[ -n "$base_name" ]]; then

        echo "Searching for files matching pattern $base_name..."
        files=$(find "$log_dir" -type f -name "*$base_name*_*_target_file_coverage*")
        
        for file in $files; do
            if [[ -f "$file" ]]; then
                cov_file_name=$(basename $file)
                echo "Processing $cov_file_name"
                fuzzer_name=$(echo $cov_file_name | cut -d'_' -f1)
                target_name=$(echo $cov_file_name | cut -d'_' -f2-4)
                temp_name=$(echo $cov_file_name | cut -d'_' -f5-)
                program_name="${temp_name%_*_target_file_coverage.txt}"
                iter_num="$(echo $cov_file_name | rev | cut -d'_' -f4 | rev)"  

                # echo "Check"
                # echo $fuzzer_name
                # echo $target_name
                # echo $program_name
                # echo $iter_num

                mkdir -p $output_path/$fuzzer_name
                result_path="${output_path}/${fuzzer_name}/${fuzzer_name}_${target_name}_${program_name}_target_function_coverage"

                if [[ ! -f "$result_path" ]]; then 
                    echo "TARGET,PROGRAM,ITER,Filename,Regions,Miss,Cover,Lines,Miss,Cover,Branches,Miss,Cover" > "$result_path"
                fi

                if [[ "$target_name" == *"openssl_10_5"* ]]; then 
                    output=$(tail -n 1 "$file" | sed -r 's/\s+/,/g')
                else
                    output=$(grep -w "$function_name" "$file" | sed 's/  \+/,/g')
                fi
                echo "$target_name,$program_name,$iter_num,$output" >> "$result_path"
            fi
        done
    fi

done < "$csv_file"
