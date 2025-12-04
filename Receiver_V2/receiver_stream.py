import serial
import time
import sys
import cv2
import numpy as np

MAGIC = b"\xAB\xCD\xEF"

if len(sys.argv) < 2:
    print("Usage: python3 receiver_stream.py <receiver_serial_port>")
    sys.exit(1)

port = sys.argv[1]

ser = serial.Serial(port, 115200, timeout=1)
time.sleep(0.3)
ser.reset_input_buffer()

print("[RECEIVER] Waiting for frames...")

while True:
    # 1️⃣ Wait for MAGIC header
    sync = bytearray()
    while True:
        b = ser.read(1)
        if not b:
            continue
        sync += b
        if len(sync) > 3:
            sync = sync[-3:]
        if sync == MAGIC:
            break

    # 2️⃣ Read version
    version = ser.read(1)

    # 3️⃣ Read size
    size_bytes = ser.read(4)
    size = int.from_bytes(size_bytes, "big")

    # 4️⃣ Read image bytes
    data = bytearray()
    while len(data) < size:
        chunk = ser.read(size - len(data))
        if chunk:
            data.extend(chunk)

    # 5️⃣ Decode JPEG into image
    img_array = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if frame is not None:
        cv2.imshow("LIVE STREAM", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close()
cv2.destroyAllWindows()
