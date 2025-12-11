Project AES – Emotion Detection System

Project AES is a modular, real-time emotion detection engine designed to process webcam video input, predict emotional states, and provide stable outputs for adaptive AI systems. It will later be integrated into the JARVIS model to enable emotionally aware interactions.

Overview

Project AES uses DeepFace, OpenCV, MediaPipe, and TensorFlow to:

Capture live camera feed

Detect faces

Classify emotions (happy, sad, angry, fear, surprise, neutral)

Stabilize predictions through signal smoothing

Provide clean and structured outputs for larger AI agents

The architecture is intentionally modular so it can be embedded as a subsystem inside the JARVIS assistant.

Project Structure
Project-AES/
│
├── config/
│   └── emotion_config.yaml
│
├── emotion/
│   ├── adapter.py
│   ├── analyzer.py
│   ├── audio.py
│   ├── camera.py
│   ├── config.py
│   ├── face.py
│   └── __init__.py
│
├── tests/
│   └── test_emotion.py
│
├── jarvis_core.py
├── response_handler.py
├── requirements.txt
└── README.md

Features

Real-time Camera Processing

Captures live frames from webcam

Provides unified camera interface

Supports multiple devices

Emotion Detection Engine

Uses DeepFace for classification

Outputs probability distribution and dominant emotion

Handles lighting inconsistencies and prediction noise

Temporal Analysis and Smoothing

Reduces frame-to-frame fluctuation

Provides stable emotional trends

Modular Integration Layer

The EmotionAdapter bridges AES output with JARVIS

Designed to allow future conversational or behavioral adaptation

Audio Emotion (Optional)

Includes initial structure for audio-based emotion detection

Can be expanded or enabled as needed

Installation

Clone the repository:

git clone https://github.com/YOUR-USERNAME/Project-AES.git
cd Project-AES


Create a virtual environment:

python -m venv venv


Activate the environment:

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate


Install dependencies:

pip install -r requirements.txt

Running the System

Start the core module:

python jarvis_core.py


The system will:

Launch a webcam window

Detect and display your face

Show real-time emotion predictions

Produce structured data for further JARVIS integration

Configuration

All runtime parameters can be modified in:

config/emotion_config.yaml


Configurable fields include:

Model paths

Confidence thresholds

Emotion labels

Camera index

Processing intervals

Whether to enable audio or face emotion modules

Testing

Run all tests:

pytest -q

Future Integration with the JARVIS Model

Project AES is built as an independent subsystem that will later plug directly into the JARVIS architecture. The integration layer (EmotionAdapter) is designed to:

Feed emotional context into dialogue management

Adapt tone, responses, and behavior

Trigger mood-based UI changes

Enable scenario-aware decision-making

This integration will allow JARVIS to respond in a more human-aware and context-sensitive manner.

Roadmap

Expanded body and gesture detection

Multi-face emotion tracking

UI dashboard for monitoring emotional state

Audio emotion refinement

Full JARVIS synchronization interface

License

MIT License.