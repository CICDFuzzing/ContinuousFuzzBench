#!/bin/bash

# Sanity check
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_file> <output_file> <number_of_lines>"
    exit 1
fi

input_file=$1           
output_file=$2    
# The number of random lines to pick from the file
num_random_lines=$3          

# Get the total number of lines in the file
total_lines=$(wc -l < "$input_file")

# Sanity check
if [ "$num_random_lines" -gt "$total_lines" ]; then
    echo "Error: The file only has $total_lines lines, but $num_random_lines were requested."
    exit 1
fi

# Prepare the output file
cat /dev/null > "$output_file" 

lines_left=$num_random_lines

# Track selected lines
declare -A selected_lines

while [ "$lines_left" -gt 0 ]; do
    # Choose a random line from the file as the starting point
    start_line=$(shuf -i 1-"$total_lines" -n 1)
    
    # Pick a random number between 1 and lines_left
    block_size=$((RANDOM % lines_left + 1)) 
    
    if [ $((start_line + block_size - 1)) -gt "$total_lines" ]; then
    # If the code block size exceeds the file length then end the block at the end of the file
        block_size=$((total_lines - start_line + 1))
    fi

    # Get the code block
    for (( i=0; i<block_size; i++ )); do
        random_line=$((start_line + i))
        # Avoid selecting the same line of code
        if [ -z "${selected_lines[$random_line]}" ]; then
            # Save the line to the array
            selected_lines[$random_line]=1
            # Save the line
            echo "$input_file:$random_line" >> "$output_file"
        fi
    done
    
    # Decrease the number of lines left to pick
    lines_left=$((lines_left - block_size))
done

echo "Results saved to '$output_file'"
