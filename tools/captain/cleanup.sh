#!/bin/bash
for dir in /home/huicongh/ContinuousFuzzBench/seed/aflpp-experiments/ar/aflplusplus/poppler*/*/*/*; do
    # Check if the directory path contains "canaries.raw"
    if [[ "$dir" == *"canaries.raw"* || "$dir" == *"core"* ]]; then
        echo "$dir contains canaries.raw or core"
        rm -f "$dir"
    else
        # Remove all files and directories except ball.tar
        find "$dir" -mindepth 1 ! -name "ball.tar" -exec rm -rf {} + 2>/dev/null
        # Remove the directory if it's empty after removing the contents
        find "$dir" -type d -empty -exec rmdir {} +
    fi
done

for dir in /home/huicongh/ContinuousFuzzBench/seed/libfuzzer-experiments1/ar/libfuzzer/poppler*/*/*/*; do
    # Check if the directory path contains "canaries.raw"
    if [[ "$dir" == *"canaries.raw"* || "$dir" == *"core"* ]]; then
        echo "$dir contains canaries.raw or core"
        rm -f "$dir"
    else
        # Remove all files and directories except ball.tar
        find "$dir" -mindepth 1 ! -name "ball.tar" -exec rm -rf {} + 2>/dev/null
        # Remove the directory if it's empty after removing the contents
        find "$dir" -type d -empty -exec rmdir {} +
    fi
done

