#!/bin/bash
sudo ln -s ${PWD}/run.sh ~/.config/autostart
gcc -shared -o ./vgc/trigonometric_fast.so -fPIC ./vgc/trigonometric_fast.c
python -m pip install --upgrade pip
pip3 install --upgrade future lxml
pip3 install pytest
pip3 install -r requirements.txt
python3 -m pip install --upgrade pymavlink
