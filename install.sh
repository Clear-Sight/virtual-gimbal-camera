#!/bin/bash

echo "Do you want to install auto start for vgc?[y/n]:" 
read answer
case $answer in
y|Y|yes)
sudo ln -s ${PWD}/run.sh ~/.config/autostart 
echo "run.sh has been added to ~/.config/autostart. Done."
;;
*)
echo "Skipping auto start. Done."
;;
esac

gcc -shared -o ./vgc/trigonometric_fast.so -fPIC ./vgc/trigonometric_fast.c
python -m pip install --upgrade pip
pip3 install --upgrade future lxml
pip3 install pytest
pip3 install -r requirements.txt
python3 -m pip install --upgrade pymavlink
