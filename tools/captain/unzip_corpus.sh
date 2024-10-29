#!/bin/bash

for i in {0..9}; do
    dir="/home/huicongh/temp/aflgo-exp-experiments-1/ar/aflgo/*/*/$i"
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
    dir="/home/huicongh/temp/aflgo-exp-experiments-2/ar/aflgo/*/*/$i"
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
    dir="/home/huicongh/temp/aflgo-exp-experiments-3/ar/aflgo/*/*/$i"
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

