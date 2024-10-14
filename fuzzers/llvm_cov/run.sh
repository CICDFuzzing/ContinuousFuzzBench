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

# sleep 24h

# if [ ! -f $SHARED/coverage/"$INITIAL_COVERAGE_PREFIX"_total_coverage_initial.txt ]; then 
#     echo "Get the coverage of the initial seeds"

#     pushd $OUT

#     export INITIAL_CORPUS="aflpp-24h-corpus1/ar/aflplusplus/openssl/$PROGRAM/0/findings/default/queue"
#     export INITIAL_COVERAGE_PREFIX=$(echo $INITIAL_CORPUS | cut -d'/' -f3-6 | tr / _)

#     echo "The initial corpus is $INITIAL_CORPUS"

#     for file in "$TARGET/corpus/$INITIAL_CORPUS"/*; do 
#         if [ -f "$file" ]; then 
#             export LLVM_PROFILE_FILE="$(basename $file).profraw"
#             timeout 5s ./$PROGRAM $FUZZARGS $file
#         else 
#             echo "file does not exist"
#             exit 1
#         fi 
#     done

#     source "$TARGET/configrc"
#     COMMIT_PATHS=("${COMMIT_FILES[@]/#/"$TARGET/repo/"}")

#     echo "S1.Check the number of profdata"
#     ls $OUT/*.profraw | wc -l
#     llvm-profdata-14 merge *.profraw -o merged.profdata
#     llvm-cov report -instr-profile merged.profdata $PROGRAM > $SHARED/coverage/"$INITIAL_COVERAGE_PREFIX"_total_coverage_initial.txt
#     llvm-cov report -instr-profile merged.profdata $PROGRAM ${COMMIT_PATHS[@]} -show-functions > $SHARED/coverage/"$INITIAL_COVERAGE_PREFIX"_target_file_coverage_initial.txt

#     mv $OUT/*.profraw $OUT/initial_coverage/
#     echo "Check that there are no profraw"
#     ls $OUT
    
#     popd
# fi

pushd $FUZZER

./collect_coverage.sh

# for i in $(seq 0 9); do 
    # export CORPUS="afl-aflpp-libfuzzer-initial-experiments/ar/afl/$(basename $TARGET)/$PROGRAM/$i/findings/queue"
    # ./collect_coverage.sh

    # export CORPUS="afl-aflpp-libfuzzer-initial-experiments/ar/aflplusplus/$(basename $TARGET)/$PROGRAM/$i/findings/default/queue"
    # ./collect_coverage.sh

    # export CORPUS="afl-aflpp-libfuzzer-initial-experiments/ar/libfuzzer/$(basename $TARGET)/$PROGRAM/$i/final-corpus/$PROGRAM"
    # ./collect_coverage.sh

    # export CORPUS="aflgo-initial-experiments/ar/aflgo/$(basename $TARGET)/$PROGRAM/$i/findings/queue"
    # ./collect_coverage.sh

    # export CORPUS="ffd-fixed-experiments/ar/ffd/$(basename $TARGET)/$PROGRAM/$i/findings/queue"
    #./collect_coverage.sh
# done

# clean up
# rm $OUT/initial_coverage/*.prof*

popd

exit 1
