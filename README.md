# Hand Tracking LED Control

This project uses **OpenCV** and **MediaPipe** to track a user's hand in real time and control an Arduino-based LED array. Each finger corresponds to an LED, allowing finger gestures to control which LEDs are illuminated.

## Features

- Real-time hand tracking using MediaPipe
- Finger state detection (up/down)
- Serial communication between Python and an Arduino Nano
- LED control based on detected finger positions
- Optional virtual drawing mode using thumb and index finger pinch gestures

## Demonstration

### LED Control

![LED Demo](images/LEDDemoGIF.gif)

### Virtual Drawing

![Drawing Demo](images/drawingGIF2.gif)

## Hardware

- Arduino Nano
- USB webcam
- Breadboard
- LEDs
- Current-limiting resistors
- Jumper wires

## Software

- Python
- OpenCV
- MediaPipe
- PySerial
- Arduino IDE

## Installation

1. Upload `test.ino` to the Arduino Nano.
2. Connect LEDs to digital pins **2–6**, each with a current-limiting resistor and a common ground.
3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

4. Run:

```bash
python main.py
```

The webcam will open and begin tracking your hand. Raising individual fingers will control the corresponding LEDs.

## Future Improvements

- Support multiple hand gestures
- Gesture recognition using machine learning
- RGB LED control
- Additional hardware outputs (servos, relays, etc.)
