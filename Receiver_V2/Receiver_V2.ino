#include <Arduino.h>
#include <ESP8266WiFi.h>

WiFiServer server(9000);

void setup() {
  Serial.begin(115200);
  delay(300);

  WiFi.softAP("ImageLink", "12345678");
  server.begin();

  // NO SERIAL PRINTS AFTER THIS
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;

  while (client.connected()) {
    while (client.available()) {
      uint8_t b = client.read();
      Serial.write(b);
    }
    delay(1);
  }

  client.stop();
}
