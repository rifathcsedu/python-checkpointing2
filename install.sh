#!/bin/bash  
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python3.6 python3.6-dev -y
python3.6 -m pip install cython
python3.6 -m pip install .
