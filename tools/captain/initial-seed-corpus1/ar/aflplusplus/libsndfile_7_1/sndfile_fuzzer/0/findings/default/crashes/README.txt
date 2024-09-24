Command line used to find this crash:

/magma/fuzzers/aflplusplus/repo/afl-fuzz -m none -t 10000 -i /magma/targets/libsndfile_7_1/corpus/sndfile_fuzzer -o /magma_shared/findings -c /magma_out/cmplog/sndfile_fuzzer -d -- /magma_out/afl/sndfile_fuzzer @@

If you can't reproduce a bug outside of afl-fuzz, be sure to set the same
memory limit. The limit used for this fuzzing session was 0 B.

Need a tool to minimize test cases before investigating the crashes or sending
them to a vendor? Check out the afl-tmin that comes with the fuzzer!

Found any cool bugs in open-source tools using afl-fuzz? If yes, please drop
an mail at <afl-users@googlegroups.com> once the issues are fixed

  https://github.com/AFLplusplus/AFLplusplus

