import random
import time
import msgpack
import paho.mqtt.client as mqtt

# =========================
# CONFIG
# =========================
BROKER = "broker.emqx.io"
PORT = 1883

BASE_ID = 1477979848
NUM_DEVICES = 5

# Per-device config (like mqttEnable in ESP32)
device_config = {
    BASE_ID + i: {
        "temperature": True,
        "battVolt": True,
        "oilPressure": True,
        "rpm": True
    }
    for i in range(NUM_DEVICES)
}

# =========================
# CALLBACKS
# =========================
def on_connect(client, userdata, flags, rc):
    print("Connected:", rc)

    if rc == 0:
        client.subscribe("iot/+/mt/cfg")
        print("Subscribed to iot/+/mt/cfg")
    else:
        print("Connection failed")


def on_disconnect(client, userdata, rc):
    print("Disconnected:", rc)


def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        print("\nIncoming:", topic)

        parts = topic.split("/")
        if len(parts) < 4:
            return

        uid = int(parts[1])
        msg_type = parts[3]

        if msg_type != "cfg":
            return

        # ✅ Decode MessagePack
        cfg = msgpack.unpackb(msg.payload, raw=False)

        print(f"CFG (MsgPack) for {uid}:", cfg)

        if uid in device_config:
            # Update ONLY this device
            device_config[uid].update({
                "temperature": cfg.get("temperature", device_config[uid]["temperature"]),
                "battVolt": cfg.get("battVolt", device_config[uid]["battVolt"]),
                "oilPressure": cfg.get("oilPressure", device_config[uid]["oilPressure"]),
                "rpm": cfg.get("rpm", device_config[uid]["rpm"]),
            })

            print(f"Updated config for {uid}: {device_config[uid]}")
        else:
            print("Unknown device:", uid)

    except Exception as e:
        print("Error:", e)


# =========================
# MAIN LOOP
# =========================
def main():
    client = mqtt.Client(client_id="msgpack-simulator")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Auto reconnect backoff
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    print("Connecting...")
    client.connect(BROKER, PORT, 60)

    # Start MQTT background loop
    client.loop_start()

    try:
        while True:
            for i in range(NUM_DEVICES):
                device_id = BASE_ID + i
                topic = f"iot/{device_id}/mo/cbor"

                cfg = device_config[device_id]
                payload = {}

                # Generate telemetry based on config
                if cfg["temperature"]:
                    payload["temperature"] = round(random.uniform(25, 30), 2)

                if cfg["battVolt"]:
                    payload["voltage"] = round(random.uniform(12.1, 13.0), 2)

                if cfg["oilPressure"]:
                    payload["pressure"] = random.randint(100, 150)

                if cfg["rpm"]:
                    payload["rpm"] = random.randint(1000, 1500)

                # Encode MessagePack
                packed = msgpack.packb(payload)

                print(f"Publish → {topic}: {payload}")
                client.publish(topic, packed)

                time.sleep(5)

    except KeyboardInterrupt:
        print("Stopping...")

    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()