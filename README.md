 # 🏎️ Asphalt 8 AI Gesture Controller (Pure Python)

An AI-powered desktop game controller built specifically for **Asphalt 8** (and other arcade racing games). It tracks your hand gestures in real-time using a webcam and converts them into hardware-level keyboard inputs using `pydirectinput` to bypass Windows game security/DirectX sandboxing.

---

## 🛠️ How the Gestures Work (Control Map)

The controller counts the **total number of extended fingers** on a single hand to trigger game actions:

| Hand Gesture | Extended Fingers | Game Action | Key Simulating |
| :--- | :---: | :--- | :---: |
| ✊ **Closed Fist** | `0` | **Accelerate / Nitro** | `W` |
| ☝️ **Index Finger Up** | `1` | **Steer Left** | `A` |
| ✌️ **Two Fingers Up** | `2` | **Steer Right** | `D` |
| 🖐️ **Full Open Palm** | `5` | **Brake / Drift / Reverse** | `S` |
| 🚫 *Any other state* | *Otherwise* | **Coasting (Neutral)** | *None Released* |

---

## ✨ Features Added in this Script

* **DirectInput Hardware Emulation:** Uses `pydirectinput` instead of regular `pyautogui`. This allows the keystrokes to work perfectly inside full-screen DirectX/3D games like Asphalt 8.
* **Always-on-Top Floating Window:** The webcam feed utilizes `WND_PROP_TOPMOST` so it stays pinned as an overlay on top of your game while you play.
* **Dynamic Thumb Tracking:** Detects thumb positioning accurately by automatically calculating coordinates based on your hand's orientation (Left Hand vs Right Hand mirroring).
* **Safety Pause Buffer:** Features a `0.05s` keypress delay configuration ensuring inputs register properly within high-frame-rate arcade engines.

---

## 💻 System Setup & Requirements

Make sure you have Python 3.11+ ready.

### 1. Install Project Dependencies
Run this exact command in your terminal to avoid any MediaPipe/Protobuf architecture mismatch versions:
```bash
pip install opencv-python mediapipe==0.10.9 pydirectinput

2. File Directory Structure

Plaintext
├── game_control.py   # Paste your provided python code here
└── README.md         # This documentation file

🎮 How to Launch & Play

Plug in your webcam and navigate to your project path.
Run the Python controller script:

```bash
python game_control.py
Wait for the terminal to print: "Asphalt 8 Controller Ready!"

Launch Asphalt 8 on your PC.

The tracking panel will float on top of your screen. Click inside the game window to focus it, show your hand to the camera, and start racing!

💡 To exit the controller application, focus the webcam window screen and press the 'q' key.
