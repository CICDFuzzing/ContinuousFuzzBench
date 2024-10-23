#!/bin/bash

# for i in {0..9}; do
#     dir="/home/huicongh/ContinuousFuzzBench/seed/afl-experiments-and-php/ar/afl/php*/*/$i"
    
#     # Use a loop to handle multiple matches
#     for subdir in $dir; do
#         if [[ -f "$subdir/ball.tar" ]]; then
#             echo "Unzipping ball.tar in $subdir"
#             tar -xf "$subdir/ball.tar" -C "$subdir"
#         else
#             echo "ball.tar not found in $subdir"
#         fi
#     done
# done

for i in {0..9}; do
    dir="/home/huicongh/ContinuousFuzzBench/seed/afl-experiments-and-php/ar/ffd/php*/*/$i"
    
    # Use a loop to handle multiple matches
    for subdir in $dir; do
        if [[ -f "$subdir/ball.tar" ]]; then
            echo "Unzipping ball.tar in $subdir"
            tar -xf "$subdir/ball.tar" -C "$subdir"
        else
            echo "ball.tar not found in $subdir"
        fi
    done
done

# for i in {0..9}; do
#     dir="/home/huicongh/ContinuousFuzzBench/seed/ffd-experiments/ar/ffd/php*/*/$i"
    
#     # Use a loop to handle multiple matches
#     for subdir in $dir; do
#         if [[ -f "$subdir/ball.tar" ]]; then
#             echo "Unzipping ball.tar in $subdir"
#             tar -xf "$subdir/ball.tar" -C "$subdir"
#         else
#             echo "ball.tar not found in $subdir"
#         fi
#     done
# done
