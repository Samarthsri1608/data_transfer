<h1>Wireless Image Transfer System Using ESP8266 & Python</h1>
<h2>📌 Project Overview</h2>

This project implements a custom wireless data transfer protocol that enables sending binary files (such as images) between two ESP8266 modules without any external Wi-Fi network or internet connection.

A Python script on the sender side reads an image (or any binary data), sends it to the Sender ESP via USB serial, which then transmits it wirelessly to the Receiver ESP using its SoftAP Wi-Fi mode. The Receiver ESP forwards the data to another Python script through USB serial, which reconstructs the image and displays it.

This creates a complete offline wireless communication system with synchronized data framing, binary streaming, and real-time image transfer.

<h2>🚀 Key Features</h2>
✅ 1. Fully Offline Wireless Communication

The ESP8266 Receiver operates as a Wi-Fi SoftAP.
The Sender ESP connects directly — no router required.

✅ 2. Custom Binary Transfer Protocol

All image files are transmitted using a robust protocol:

MAGIC (3 bytes)  → AB CD EF
VERSION (1 byte) → 01
SIZE (4 bytes)   → Big-endian file length
DATA (N bytes)   → Raw image bytes


This ensures:

Proper alignment

Zero corruption

Deterministic parsing

✅ 3. Supports Any Type of Binary Data

JPEG images used for demonstration, but:

PNG

Audio

Video segments

Binary blobs

Firmware files

…all work with the same system.

✅ 4. Python-Based Control

Python handles:

File reading

Serial transfer

Stream reconstruction

Live display (via OpenCV)

✅ 5. Expandable Architecture

The system can easily be extended to:

Live Webcam Streaming

Encrypted transfers

Multi-node mesh networks

Chunk-level error correction

<h2>📡 System Architecture</h2>

```
+-----------------+      USB Serial       +-----------------+
|   Python Sender |  ------------------>  |   ESP8266 Sender|
|   (Webcam/File) |                       |  (Station Mode) |
+-----------------+                       +-----------------+
                                                 |
                                                 |  Wi-Fi TCP (SoftAP)
                                                 v
                                         +------------------+
                                         | ESP8266 Receiver |
                                         |   (SoftAP Mode)  |
                                         +------------------+
                                                 |
                                                 | USB Serial
                                                 v
                                       +-----------------------+
                                       |   Python Receiver     |
                                       | (Rebuild + Display)   |
                                       +-----------------------+
```

<h2>🧩 Project Structure </h2>

```
/project
│
├── sender_stream.py        # Webcam → Sender ESP script
├── receiver_stream.py      # Receiver ESP → Display script
│
├── sender.py               # Single-image sender script
├── receiver.py             # Single-image receiver script
│
├── esp_sender/             # PlatformIO project for Sender ESP
│   └── src/main.cpp
│
└── esp_receiver/           # PlatformIO project for Receiver ESP
    └── src/main.cpp
```

<h2>🛠 Required Hardware</h2>

2 × ESP8266 (NodeMCU recommended)

MicroUSB cables

Laptop/PC capable of running Python

Webcam (optional for live-stream mode)

🧰 Software Requirements

Python 3.x

PlatformIO (VS Code extension)

Python libraries:

pip install pyserial opencv-python pillow

<h2>⚙️ How It Works</h2>
Sender Side

Python reads a local image or webcam frame

Python sends the file size followed by raw JPEG bytes to ESP Sender

ESP Sender wraps bytes inside TCP and transmits wirelessly

Receiver Side

ESP Receiver forwards incoming bytes to Python Receiver

Python Receiver synchronizes using MAGIC header

Reads full file

Reconstructs image

Displays it live

<h2>🚀 Running the Project</h2> 

1️⃣ Flash ESP Receiver
```
Using PlatformIO:

Upload → esp_receiver project
```

Then open:

python3 receiver_stream.py /dev/ttyUSB_RECEIVER

2️⃣ Flash ESP Sender
```
Using PlatformIO:

Upload → esp_sender project
```

3️⃣ Start Webcam Streaming
```
python3 sender_stream.py /dev/ttyUSB_SENDER
```

A live video window opens on the receiver side.

<h2>🧪 Sample Output</h2>

Live image displayed from the webcam

Verified file size and clean frame reconstruction

Zero corruption due to header sync

Offline wireless communication established successfully

<h2>🧠 Challenges Solved</h2>

Serial/Wi-Fi synchronization

ESP boot-noise buffer flushing

Binary alignment issues

Custom packet framing

Efficient TCP-based streaming

<h2>🎯 Conclusion</h2>

This project demonstrates a fully functional wireless communication pipeline built from scratch using ESP8266 modules and Python.

It highlights skills in:

Networking

Embedded systems

Protocol design

Data streaming

Python–MCU integration

Perfect for a major project or technical showcase.

<h2>⭐ Future Enhancements</h2>

CRC32 or SHA-256 integrity verification

AES encrypted transmission

Multi-device broadcast

Chunk acknowledgment + retransmission

Video compression

High FPS streaming with ESP32