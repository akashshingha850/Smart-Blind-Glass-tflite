#!/bin/bash
cd /home/pi/.virtualenvs/cv/bin
source activate

cd /home/pi/object_detection_tflite

for (( ; ; ))
do

  python3 object_speak.py

done

   

