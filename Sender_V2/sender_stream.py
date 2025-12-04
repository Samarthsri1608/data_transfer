import cv2
import serial
import struct
import time
import sys

if len(sys.argv) < 2:
    print("Usage: python3 sender_stream.py <sender_serial_port>")
    sys.exit(1)

port = sys.argv[1]

# Open serial to Sender ESP
ser = serial.Serial(port, 115200, timeout=1)
time.sleep(0.3)

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 320)   # width
cap.set(4, 240)   # height

print("[SENDER] Webcam streaming started. Press Ctrl+C to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # JPEG compress frame
    ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
    data = jpeg.tobytes()
    size = len(data)

    # Send size first (4 bytes)
    ser.write(struct.pack(">I", size))

    # Stream bytes
    sent = 0
    CHUNK = 1024

    while sent < size:
        chunk = data[sent:sent+CHUNK]
        ser.write(chunk)
        sent += len(chunk)

    ser.flush()

    # OPTIONAL: show outgoing frame locally
    cv2.imshow("SENDER local preview", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close()
cap.release()
cv2.destroyAllWindows()
