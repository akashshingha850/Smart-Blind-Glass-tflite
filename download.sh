#!/bin/bash

if [ $# -eq 0 ]; then
  DATA_DIR="/home/pi/object_detection_tflite"
else
  DATA_DIR="$1"
fi

# Install required packages
python3 -m pip install -r requirements.txt
pyyhon3 -m pip install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
pyyhon3 -m pip install RPi.GPIO
# Get TF Lite model and labels
curl -O http://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
unzip coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip -d ${DATA_DIR}
rm coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip

# Get a labels file with corrected indices, delete the other one
(cd ${DATA_DIR} && curl -O  https://dl.google.com/coral/canned_models/coco_labels.txt)
rm ${DATA_DIR}/labelmap.txt

# Get version compiled for Edge TPU
#(cd ${DATA_DIR} && curl -O  https://dl.google.com/coral/canned_models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite)

echo -e "Files downloaded to ${DATA_DIR}"
