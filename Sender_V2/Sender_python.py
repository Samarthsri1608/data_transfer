import serial, struct, time, sys, os

if len(sys.argv) < 3:
    print("Usage: python3 sender.py <image_file> <sender_serial_port>")
    sys.exit(1)

image_path = sys.argv[1]
port = sys.argv[2]

with open(image_path, "rb") as f:
    data = f.read()

size = len(data)
print(f"[SENDER] Image size = {size}")

ser = serial.Serial(port, 115200, timeout=1)
time.sleep(0.3)  # allow ESP to stabilize

# Send 4-byte size
ser.write(struct.pack(">I", size))
ser.flush()

CHUNK = 1024
sent = 0
print("[SENDER] Sending...")

while sent < size:
    chunk = data[sent:sent+CHUNK]
    ser.write(chunk)
    sent += len(chunk)
    print(f"\rSent {sent}/{size}", end="")

ser.flush()
ser.close()
print("\n[SENDER] Done.")
