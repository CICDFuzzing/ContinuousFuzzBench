#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##


git clone --no-checkout https://github.com/prosyslab/DAFL.git "$FUZZER/repo"
git -C "$FUZZER/repo" checkout 50d68fc44948ab3b25a7af2f5fc9918110b1939a
