# Adaptive Traffic Lights AI System

The Adaptive Traffic Lights AI System (ATLAS) is an intelligent traffic management solution that uses computer vision to analyze traffic conditions at a four-way junction and adjust signal timings accordingly.

## Overview

The system employs state-of-the-art vehicle detection and tracking techniques to monitor traffic flow in real-time. By dynamically analyzing the number and types of vehicles present at each side of the junction, the system optimizes signal timings to minimize congestion and improve overall traffic efficiency.

## Features

- Real-time vehicle detection and tracking using YOLOv4-tiny model.
- Dynamic adjustment of signal timings based on traffic analysis.
- Modular design for easy integration with existing traffic control systems.
- Scalable architecture to accommodate varying traffic volumes and junction configurations.

## Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- NumPy (`numpy`)

## Usage

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/your-username/adaptive-traffic-lights.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Place the YOLOv4-tiny model files (`yolov4-tiny.weights`, `yolov4-tiny.cfg`) and the class names file (`coco.names`) in the project directory.

4. Update the video sources in `main.py` to point to the video streams for each side of the junction.

5. Run `main.py` to start the Adaptive Traffic Lights AI System:

    ```bash
    python main.py
    ```

