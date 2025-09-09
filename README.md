# Smart Blind Glasses: Real-Time Object Detection and Navigation Assistance System for Visually Impaired Using TensorFlow Lite

This project implements an intelligent assistive device for visually impaired users using [TensorFlow Lite](https://tensorflow.org/lite) on a Raspberry Pi. The Smart Blind Glass system combines multiple technologies to provide real-time environmental awareness through audio feedback.

## Features

- **Real-time Object Detection**: Uses TensorFlow Lite to identify objects in the environment via Pi Camera
- **Audio Feedback**: Text-to-speech announcements of detected objects using espeak
- **Ultrasonic Distance Sensing**: Dual sonar sensors for obstacle detection and distance measurement
- **Smart Notifications**: Email integration and clock functionality
- **Lightweight**: Optimized for Raspberry Pi with minimal resource usage

The system is designed to be worn as smart glasses, providing hands-free navigation assistance and environmental awareness for visually impaired users.

## Hardware Requirements

- Raspberry Pi (3B+ or 4 recommended)
- Pi Camera Module
- HC-SR04 Ultrasonic Sensors (2x)
- Speaker or headphones for audio output
- Jumper wires and breadboard for connections

Optional: Coral USB Accelerator for enhanced performance (~10x speed increase)


## Hardware Setup

### Raspberry Pi Setup
Before you begin, you need to [set up your Raspberry Pi](
https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up) with
Raspbian (preferably updated to Buster or later).

### Pi Camera Configuration
[Connect and configure the Pi Camera](
https://www.raspberrypi.org/documentation/configuration/camera.md) module.

### Ultrasonic Sensor Wiring
Connect the HC-SR04 ultrasonic sensors as follows:
- **Sensor 1**: Trigger Pin 18, Echo Pin 24
- **Sensor 2**: Trigger Pin 17, Echo Pin 27
- **Power**: 5V and GND connections

### Audio Output
Ensure you have speakers or headphones connected to the Pi's audio output for text-to-speech feedback.

### Display (Optional)
A monitor can be connected to see the camera feed with bounding boxes during development/testing.


## Installation

### Install TensorFlow Lite Runtime

This project uses the lightweight `tflite_runtime` package instead of the full TensorFlow package for better performance on Raspberry Pi.

Follow the instructions in the [Python quickstart](https://www.tensorflow.org/lite/guide/python) to install TensorFlow Lite runtime.

### Install Additional Dependencies

Install required system packages:
```bash
sudo apt update
sudo apt install espeak espeak-data libespeak1 libespeak-dev
```

### Download the Project

Clone this repository onto your Raspberry Pi:

```bash
git clone https://github.com/akashshingha850/Smart-Blind-Glass-tflite.git
cd Smart-Blind-Glass-tflite
```

### Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Download Models and Setup

Run the setup script to download the TensorFlow Lite model and labels:

```bash
bash download.sh
```

### Make Scripts Executable

```bash
chmod +x object_detection.sh
chmod +x object_speak.sh
```

## Usage

### Basic Object Detection

Run the basic object detection with visual display:

```bash
python3 detect_picamera.py \
  --model ./model/detect.tflite \
  --labels ./label/coco_labels.txt
```

### Smart Glass Mode (Audio-Only)

For hands-free operation with audio feedback:

```bash
python3 object_speak.py
```

This mode provides:
- Object detection with spoken announcements
- Distance measurement using ultrasonic sensors
- Audio feedback for navigation assistance

### Additional Features

- **Clock functionality**: `python3 clock.py`
- **Distance sensing**: `python3 sonar.py`
- **Email integration**: `python3 mail.py`
- **Text processing**: `python3 write_text.py`

### Shell Scripts

Use the provided shell scripts for automated execution:
- `./object_detection.sh` - Basic object detection
- `./object_speak.sh` - Audio-enhanced smart glass mode

The system will announce detected objects and provide distance information through audio feedback, making it ideal for visually impaired users to navigate their environment safely.


## Performance Optimization (Optional)

### Coral USB Accelerator Support

For significantly faster inference speeds, you can use the [Coral USB Accelerator](
https://coral.withgoogle.com/products/accelerator) with Edge TPU support.

#### Setup Steps:

1. Complete the [USB Accelerator setup instructions](
   https://coral.withgoogle.com/docs/accelerator/get-started/).

2. Modify `detect_picamera.py` to use the Edge TPU delegate:

   Add the import:
   ```python
   from tflite_runtime.interpreter import load_delegate
   ```

   Update the interpreter initialization:
   ```python
   interpreter = Interpreter(args.model,
       experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
   ```

3. Use the Edge TPU-compiled model:
   ```bash
   python3 detect_picamera.py \
     --model /tmp/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
     --labels /tmp/coco_labels.txt
   ```

This optimization can improve inference speeds by up to 10x, making the real-time object detection more responsive for assistive applications.

## Project Structure

```
Smart-Blind-Glass-tflite/
├── detect_picamera.py      # Main object detection script
├── object_speak.py         # Audio-enhanced detection
├── sonar.py               # Ultrasonic distance sensing
├── clock.py               # Clock functionality
├── mail.py                # Email integration
├── write_text.py          # Text processing
├── annotation.py          # Object annotation utilities
├── model/                 # TensorFlow Lite models
├── label/                 # Object classification labels
├── requirements.txt       # Python dependencies
└── *.sh                  # Shell scripts for automation
```

## Contributing

This project is designed to assist visually impaired users. Contributions that improve accessibility, performance, or add new assistive features are welcome.

## License

This project builds upon TensorFlow Lite examples and is intended for educational and assistive technology purposes.

## Acknowledgments

- TensorFlow Lite team for the base object detection framework
- Raspberry Pi Foundation for the platform
- Contributors to assistive technology development

## Citation

If you use this project in your research or work, please cite the following papers:

1. **Development of a Microprocessor Based Smart and Safety Blind Glass SystemMicroprocessor-Based Smart Blind Glass System for Visually Impaired People**  
  DOI: [10.1109/ICAECT49130.2020.9036504](https://ieeexplore.ieee.org/document/9036504)

```bibtex
@InProceedings{10.1007/978-981-13-7564-4_13,
author="Islam, Md. Tobibul
and Ahmad, Mohiuddin
and Bappy, Akash Shingha",
editor="Uddin, Mohammad Shorif
and Bansal, Jagdish Chand",
title="Microprocessor-Based Smart Blind Glass System for Visually Impaired People",
booktitle="Proceedings of International Joint Conference on Computational Intelligence",
year="2020",
publisher="Springer Nature Singapore",
address="Singapore",
pages="151--161",
isbn="978-981-13-7564-4"
}
```   

2. **Microprocessor-Based Smart Blind Glass System for Visually Impaired People**  
   DOI: [10.1007/978-981-13-7564-4_13](https://link.springer.com/chapter/10.1007/978-981-13-7564-4_13)



```bibtex
@INPROCEEDINGS{9036504,
  author={Islam, Md.Tobibul and Ahmad, Mohiuddin and Bappy, Akash shingha},
  booktitle={2019 International Conference on Computer, Communication, Chemical, Materials and Electronic Engineering (IC4ME2)}, 
  title={Development of a Microprocessor Based Smart and Safety Blind Glass System}, 
  year={2019},
  volume={},
  number={},
  pages={1-4},
  keywords={Global Positioning System;Safety;Smart glasses;Google;Floors;Tracking;Smart blind glass;Safety System;microprocessor-based control;real-time tracking;Visually impaired people},
  doi={10.1109/IC4ME247184.2019.9036504}}

``` 