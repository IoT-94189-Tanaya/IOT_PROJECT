// include required libraries
#include <WiFi.h>
#include <ArduinoMqttClient.h>
#include <DHT.h>
// Define sensor pins and types
#define DHTPIN 4
#define DHTTYPE DHT11
#define MQ2_PIN 34
// Wifi and MQTT configuration
const char* ssid = "Tanaya's S24";
const char* password = "Tanaya@2911";
const char* mqtt_server="192.168.6.2";
const char* broker = "test.mosquitto.org";
int port = 1883;
const char* topic = "env/data";
// Create wifi and MQTT client objects
WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);
// Create DHT sensor object 
DHT dht(DHTPIN, DHTTYPE);
// stepup function(runs once)
void setup() {
// start serial communication
  Serial.begin(115200);
//  Initalize DHT sensor
  dht.begin();
//  Connect to wifi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  //  WiFi connected message
  Serial.println("\nWiFi Connected");
//  Connect to MQTT broker
  mqttClient.connect(broker, port);
  Serial.println("Connected to MQTT Broker");
}
//  Loop function (runs repeatedly)

void loop() {
  // Read temperature from DHT11
  float temp = dht.readTemperature();
  // Read humidity from DHT11
  float hum = dht.readHumidity();
  // Read gas value from MQ2 sensor
  int gas = analogRead(MQ2_PIN);
//Check if DHT values are valid
  if (isnan(temp) || isnan(hum)) {
    Serial.println("Failed to read DHT sensor");
    return;
  }
//Create JSON payload
  String payload = "{";
  payload += "\"temperature\":" + String(temp) + ",";
  payload += "\"humidity\":" + String(hum) + ",";
  payload += "\"gas\":" + String(gas);
  payload += "}";
//Publish data to MQTT topic
  mqttClient.beginMessage(topic);
  mqttClient.print(payload);
  mqttClient.endMessage();
// Print published data
  Serial.println("Published: " + payload);
  // Delay of 5 seconds
  delay(5000);
}