#!/bin/sh
python ../main.py test_plugin.json
mkdir build
cd build
cmake ..
make

