#include <Arduino.h>
#include <ESP8266WiFi.h>

const char* ssid = "ImageLink";
const char* password = "12345678";

IPAddress receiverIP(192,168,4,1);
uint16_t receiverPort = 9000;

WiFiClient client;

uint32_t read_size() {
  uint32_t size = 0;
  while (Serial.available() < 4) delay(1);

  for (int i = 0; i < 4; i++)
    size = (size << 8) | (Serial.read() & 0xFF);

  return size;
}

void send_header(uint32_t size) {
  uint8_t header[8] = {
      0xAB, 0xCD, 0xEF, 0x01,
      (uint8_t)(size >> 24),
      (uint8_t)(size >> 16),
      (uint8_t)(size >> 8),
      (uint8_t)size
  };
  client.write(header, 8);
}

void setup() {
  Serial.begin(115200);
  delay(300);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(100);
}

void loop() {

  if (Serial.available() >= 4) {

    uint32_t size = read_size();

    if (!client.connect(receiverIP, receiverPort)) return;

    send_header(size);

    uint32_t sent = 0;
    uint8_t buf[1024];

    while (sent < size) {
      if (Serial.available()) {
        int n = Serial.readBytes(buf, min((uint32_t)1024, size - sent));
        client.write(buf, n);
        sent += n;
      }
    }

    client.flush();
    client.stop();
  }
}
