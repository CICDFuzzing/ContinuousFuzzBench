#!/bin/bash 
set -e

for i in {0..9}; do
    dir="/home/huicongh/libfuzzer/ContinuousFuzzBench/tools/captain/libfuzzer-experiments1/ar/libfuzzer/*/*/$i"
    # Use a loop to handle multiple matches
    for subdir in $dir; do
        if [[ -f "$subdir/ball.tar" ]]; then
            echo "Unzipping ball.tar in $subdir"
            tar -xf "$subdir/ball.tar" -C "$subdir"
            rm "$subdir/ball.tar"
        else
            echo "ball.tar not found in $subdir"
        fi
    done
done

for i in {0..9}; do
    dir="/home/huicongh/libfuzzer/ContinuousFuzzBench/tools/captain/libfuzzer-experiments2/ar/libfuzzer/*/*/$i"
    # Use a loop to handle multiple matches
    for subdir in $dir; do
        if [[ -f "$subdir/ball.tar" ]]; then
            echo "Unzipping ball.tar in $subdir"
            tar -xf "$subdir/ball.tar" -C "$subdir"
            rm "$subdir/ball.tar"
        else
            echo "ball.tar not found in $subdir"
        fi
    done
done

for i in {0..9}; do
    dir="/home/huicongh/libfuzzer/ContinuousFuzzBench/tools/captain/libfuzzer-experiments3/ar/libfuzzer/*/*/$i"
    # Use a loop to handle multiple matches
    for subdir in $dir; do
        if [[ -f "$subdir/ball.tar" ]]; then
            echo "Unzipping ball.tar in $subdir"
            tar -xf "$subdir/ball.tar" -C "$subdir"
            rm "$subdir/ball.tar"
        else
            echo "ball.tar not found in $subdir"
        fi
    done
done

for i in {0..9}; do
    dir="/home/huicongh/libfuzzer/ContinuousFuzzBench/tools/captain/libfuzzer-experiments4/ar/libfuzzer/*/*/$i"
    # Use a loop to handle multiple matches
    for subdir in $dir; do
        if [[ -f "$subdir/ball.tar" ]]; then
            echo "Unzipping ball.tar in $subdir"
            tar -xf "$subdir/ball.tar" -C "$subdir"
            rm "$subdir/ball.tar"
        else
            echo "ball.tar not found in $subdir"
        fi
    done
done

