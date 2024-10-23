#!/bin/bash
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
