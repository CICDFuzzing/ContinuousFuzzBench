#!/bin/bash
set -e

apt-get update && apt-get upgrade -y
apt-get install -yy libc6-dev binutils libgcc-9-dev
apt-get install -yy \
      wget apt-transport-https git unzip \
      build-essential libtool libtool-bin gdb \
      automake autoconf bison flex python python3 sudo vim

export OUT=/out
export SRC=/src
export WORK=/work
export PATH="$PATH:$OUT"
# Create required directories
mkdir -p "$OUT" "$SRC" "$WORK"

cd "$FUZZER/src"
# Install CMake
export CMAKE_VERSION="3.21.1"
wget https://github.com/Kitware/CMake/releases/download/v$CMAKE_VERSION/cmake-$CMAKE_VERSION-Linux-x86_64.sh
chmod +x cmake-$CMAKE_VERSION-Linux-x86_64.sh
./cmake-$CMAKE_VERSION-Linux-x86_64.sh --skip-license --prefix="/usr/local"
rm cmake-$CMAKE_VERSION-Linux-x86_64.sh
rm -rf /usr/local/doc/cmake /usr/local/bin/cmake-gui
echo "Run llvm script"
./checkout_build_install_llvm.sh
echo "Finished running llvm script"

# Install packages needed for fuzzers and benchmark
apt-get update && apt-get install -yy \
      git build-essential bc \
      golang \
      libncurses5 \
      libfreetype6 libfreetype6-dev \
      python-dev \
      nasm \
      libbz2-dev liblzo2-dev \
      gcc-multilib
