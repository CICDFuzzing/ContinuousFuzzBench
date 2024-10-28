#!/bin/bash -e

parent_dir="/home/huicongh/aflgo/ContinuousFuzzBench/tools/captain/aflgo-exp-experiments-3"

for subdir in "$parent_dir"/*/*/*/*/*; do
  if [ ! -f "${subdir}/ball.tar" ]; then
    echo "ball.tar not found in $subdir"
  fi
done
