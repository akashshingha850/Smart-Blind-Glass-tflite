#!/bin/bash
cd /home/pi/.virtualenvs/tf/bin
source activate

cd /home/pi/object_detection

python3 detect_picamera.py \
  --model detect.tflite \
  --labels coco_labels.txt

