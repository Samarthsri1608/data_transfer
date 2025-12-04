import serial, sys, time
from PIL import Image
import io

MAGIC = b"\xAB\xCD\xEF"

if len(sys.argv) < 3:
    print("Usage: python3 receiver.py <receiver_serial_port> <output_file>")
    sys.exit(1)

port = sys.argv[1]
output_file = sys.argv[2]

ser = serial.Serial(port, 115200, timeout=1)
time.sleep(0.3)

# Clear ESP boot noise
ser.reset_input_buffer()

print("[RECEIVER] Waiting for header...")

# Sync on MAGIC
sync = bytearray()
while True:
    b = ser.read(1)
    if not b:
        continue
    sync += b
    if len(sync) > 3:
        sync = sync[-3:]
    if sync == MAGIC:
        print("[RECEIVER] MAGIC OK")
        break

# Version
ver = ser.read(1)
print("Version:", ver.hex())

# Size
size = int.from_bytes(ser.read(4), "big")
print("Size:", size)

# Receive bytes
data = bytearray()
print("[RECEIVER] Receiving image...")

while len(data) < size:
    chunk = ser.read(size - len(data))
    if chunk:
        data.extend(chunk)
        print(f"\rReceived {len(data)}/{size}", end="")
    else:
        time.sleep(0.001)

print("\n[RECEIVER] Done.")

# Save file
with open(output_file, "wb") as f:
    f.write(data)

print("[RECEIVER] Saved", output_file)

# Auto show
try:
    img = Image.open(io.BytesIO(data))
    img.show()
except Exception as e:
    print("Display failed:", e)
