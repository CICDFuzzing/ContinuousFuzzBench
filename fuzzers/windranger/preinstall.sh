#!/bin/bash
set -e

apt-get update
LLVM_DEP_PACKAGES="build-essential make cmake ninja-build git binutils-gold binutils-dev curl wget python3"
apt-get install -y $LLVM_DEP_PACKAGES

apt-get update
apt-get install -y python3-dev python3-pip pkg-config autoconf automake libtool-bin gawk libboost-all-dev

python3 -m pip install --upgrade pip
# See https://networkx.org/documentation/stable/release/index.html
case `python3 -c 'import sys; print(sys.version_info[:][1])'` in
    [01])
        python3 -m pip install 'networkx<1.9';;
    2)
        python3 -m pip install 'networkx<1.11';;
    3)
        python3 -m pip install 'networkx<2.0';;
    4)
        python3 -m pip install 'networkx<2.2';;
    5)
        python3 -m pip install 'networkx<2.5';;
    6)
        python3 -m pip install 'networkx<2.6';;
    7)
        python3 -m pip install 'networkx<2.7';;
    8)
        python3 -m pip install 'networkx<=3.1';;
    *)
        python3 -m pip install networkx;;
esac
python3 -m pip install pydot pydotplus

apt-get update && \
    apt-get install -y make build-essential clang-12  lld-12 git wget

update-alternatives \
  --install /usr/lib/llvm              llvm             /usr/lib/llvm-12  20 \
  --slave   /usr/bin/llvm-config       llvm-config      /usr/bin/llvm-config-12  \
    --slave   /usr/bin/llvm-ar           llvm-ar          /usr/bin/llvm-ar-12 \
    --slave   /usr/bin/llvm-as           llvm-as          /usr/bin/llvm-as-12 \
    --slave   /usr/bin/llvm-bcanalyzer   llvm-bcanalyzer  /usr/bin/llvm-bcanalyzer-12 \
    --slave   /usr/bin/llvm-c-test       llvm-c-test      /usr/bin/llvm-c-test-12 \
    --slave   /usr/bin/llvm-cov          llvm-cov         /usr/bin/llvm-cov-12 \
    --slave   /usr/bin/llvm-diff         llvm-diff        /usr/bin/llvm-diff-12 \
    --slave   /usr/bin/llvm-dis          llvm-dis         /usr/bin/llvm-dis-12 \
    --slave   /usr/bin/llvm-dwarfdump    llvm-dwarfdump   /usr/bin/llvm-dwarfdump-12 \
    --slave   /usr/bin/llvm-extract      llvm-extract     /usr/bin/llvm-extract-12 \
    --slave   /usr/bin/llvm-link         llvm-link        /usr/bin/llvm-link-12 \
    --slave   /usr/bin/llvm-mc           llvm-mc          /usr/bin/llvm-mc-12 \
    --slave   /usr/bin/llvm-nm           llvm-nm          /usr/bin/llvm-nm-12 \
    --slave   /usr/bin/llvm-objdump      llvm-objdump     /usr/bin/llvm-objdump-12 \
    --slave   /usr/bin/llvm-ranlib       llvm-ranlib      /usr/bin/llvm-ranlib-12 \
    --slave   /usr/bin/llvm-readobj      llvm-readobj     /usr/bin/llvm-readobj-12 \
    --slave   /usr/bin/llvm-rtdyld       llvm-rtdyld      /usr/bin/llvm-rtdyld-12 \
    --slave   /usr/bin/llvm-size         llvm-size        /usr/bin/llvm-size-12 \
    --slave   /usr/bin/llvm-stress       llvm-stress      /usr/bin/llvm-stress-12 \
    --slave   /usr/bin/llvm-symbolizer   llvm-symbolizer  /usr/bin/llvm-symbolizer-12 \
    --slave   /usr/bin/llvm-tblgen       llvm-tblgen      /usr/bin/llvm-tblgen-12

update-alternatives \
  --install /usr/bin/clang                 clang                  /usr/bin/clang-12     20 \
  --slave   /usr/bin/clang++               clang++                /usr/bin/clang++-12 \
  --slave   /usr/bin/clang-cpp             clang-cpp              /usr/bin/clang-cpp-12
