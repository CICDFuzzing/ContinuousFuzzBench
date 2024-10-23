#!/bin/bash

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
# - env TARGET: path to target work dir
# - env OUT: path to directory where artifacts are stored
# - env SHARED: path to directory shared with host (to store results)
# - env PROGRAM: name of program to run (should be found in $OUT)
# - env ARGS: extra arguments to pass to the program
# - env FUZZARGS: extra arguments to pass to the fuzzer
##

echo "No fuzzer included. This is just for building an analysis target."

mkdir -p $SHARED/coverage
pushd $FUZZER
for i in $(seq 0 9); do 
    export CORPUS="$SEED/afl/$PROGRAM/$i/findings/queue"
    ./collect_coverage.sh $i afl

    export CORPUS="$SEED/ffd/$PROGRAM/$i/findings/queue"
    ./collect_coverage.sh $i ffd
done
popd

exit 1
