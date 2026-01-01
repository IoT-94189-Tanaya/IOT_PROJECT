import json
import mysql.connector
import paho.mqtt.client as mqtt
import requests

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="smart_env"
)
cursor = db.cursor()

# ---------------- THINGSPEAK CONFIG ----------------
THINGSPEAK_API_KEY = "U81NDWWWLNRQW35T"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# ---------------- MQTT CALLBACKS ----------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe("env/data")
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        temperature = data["temperature"]
        humidity = data["humidity"]
        gas = data["gas"]

        # -------- Store in MySQL --------
        sql = """
        INSERT INTO sensor_data (temperature, humidity, gas)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (temperature, humidity, gas))
        db.commit()

        print("Received & Stored:", data)

        # -------- Send to ThingSpeak --------
        payload = {
            "api_key": THINGSPEAK_API_KEY,
            "field1": temperature,
            "field2": humidity,
            "field3": gas
        }
        requests.post(THINGSPEAK_URL, data=payload)

        print("Sent to ThingSpeak")

    except Exception as e:
        print("Error:", e)

# ---------------- MQTT CLIENT ----------------
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "env/data")

client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()