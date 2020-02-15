#!/bin/bash
cd /home/pi/.virtualenvs/cv/bin
source activate

cd /home/pi/object_detection_tflite

for (( ; ; ))
do

  python3 detect_picamera.py \
    --model ./model/detect.tflite \
    --labels ./label/coco_labels.txt

done

   

