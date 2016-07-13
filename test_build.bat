@echo off
rmdir -rf example
mkdir example
cd example
python ../main.py ../test_plugin.json -folder .
mkdir build
cd build
cmake -G "Visual Studio 14 2015 Win64" ..


