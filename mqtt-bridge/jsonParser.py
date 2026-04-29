import json
import msgpack
import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io"
PORT = 1883

SUB_TOPICS = [
    ("iot/+/mo/msgpack", 0),
    ("iot/+/mo/cfg", 0)
]

# =========================
# CALLBACKS
# =========================
def on_connect(client, userdata, flags, rc):
    print("Connected:", rc)

    if rc == 0:
        for topic, qos in SUB_TOPICS:
            client.subscribe(topic)
            print(f"Subscribed to {topic}")
    else:
        print("Connection failed")


def on_disconnect(client, userdata, rc):
    print("Disconnected, rc:", rc)


def on_message(client, userdata, msg):
    try:
        parts = msg.topic.split("/")
        if len(parts) < 4:
            return

        uid = parts[1]
        msg_type = parts[3]

        # =========================
        # DEVICE TELEMETRY (MessagePack)
        # =========================
        if msg_type == "cbor":
            data = msgpack.unpackb(msg.payload, raw=False)
            print("MessagePack decoded:", data)

            json_payload = json.dumps(data)
            print(f"Publishing JSON → iot/{uid}/mt/msg: {json_payload}")

            client.publish(f"iot/{uid}/mt/msg", json_payload)

        # =========================
        # CONFIG (JSON → CBOR or JSON passthrough)
        # =========================
        elif msg_type == "cfg":
            # 1. Decode JSON payload from device/cloud
            cfg = json.loads(msg.payload.decode())

            print("Received CFG (JSON):", cfg)

            # 2. Convert JSON → MessagePack
            msgpack_payload = msgpack.packb(cfg, use_bin_type=True)

            print(f"Publishing CFG (MsgPack) → iot/{uid}/mt/cfg")

            # 3. Publish binary MessagePack
            client.publish(f"iot/{uid}/mt/cfg", msgpack_payload)

    except Exception as e:
        print("Error:", e)


# =========================
# MAIN
# =========================
def main():
    client = mqtt.Client(client_id="python-bridge")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.reconnect_delay_set(min_delay=1, max_delay=30)

    print("Connecting once...")
    client.connect(BROKER, PORT, 60)

    client.loop_forever()


if __name__ == "__main__":
    main()