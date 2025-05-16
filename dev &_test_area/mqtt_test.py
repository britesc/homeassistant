import paho.mqtt.client as mqtt

# MQTT Broker Configuration
BROKER = "192.168.8.70"  # Change to your broker address
PORT = 1883  # Default MQTT port (use 8883 for TLS)
TOPIC = "homeassistant/julian/medicine/drugname/expiry"
PAYLOAD = "04/04/2025"  # Example payload
QOS = 1  # Quality of Service level (0, 1, or 2)
RETAIN = True  # Retain flag enabled

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

# Create MQTT client instance
client = mqtt.Client()

# Assign event callbacks
client.on_connect = on_connect

# Connect to MQTT Broker
client.connect(BROKER, PORT, 60)

# Publish message with RETAIN flag
result = client.publish(TOPIC, PAYLOAD, qos=QOS, retain=RETAIN)

# Check if message was published successfully
if result.rc == mqtt.MQTT_ERR_SUCCESS:
    print(f"Message '{PAYLOAD}' published to topic '{TOPIC}' with RETAIN={RETAIN}")
else:
    print("Failed to publish message.")

# Disconnect
client.disconnect()
