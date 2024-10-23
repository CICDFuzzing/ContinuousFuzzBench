#!/bin/bash
<<<<<<< HEAD
#openssl_11_4 openssl_11_6 openssl_17_2 openssl_17_4 openssl_18_5 openssl_19_1 openssl_20_3 openssl_20_4
for i in {0..9}; do
    dir="/home/huicongh/ContinuousFuzzBench/seed/afl/poppler*/*/$i"
    
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

for i in {0..9}; do
    dir="/home/huicongh/ContinuousFuzzBench/seed/ffd/poppler*/*/$i"
=======

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
>>>>>>> 2c2bc52b83f41d703da9971afbb3973547fd4e03
    
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
