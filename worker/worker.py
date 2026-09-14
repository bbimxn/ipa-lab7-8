import json
import os
import time
from datetime import datetime, timezone

import pika
from bson import json_util
from dotenv import load_dotenv
from netmiko import ConnectHandler
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
DB_NAME = os.environ.get("DB_NAME", "ipa2026_db")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.environ.get("RABBITMQ_DEFAULT_USER", "guest")
RABBITMQ_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS", "guest")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
interface_status = db["interface_status"]


def check_interfaces(router):
    device = {
        "device_type": "cisco_ios",
        "host": router["ip"],
        "username": router["username"],
        "password": router["password"],
    }
    connection = ConnectHandler(**device)
    output = connection.send_command("show ip interface brief", use_textfsm=True)
    connection.disconnect()
    return output


def on_message(channel, method, properties, body):
    router = json_util.loads(body)
    print(f"Received job for router {router.get('ip')}")

    try:
        interfaces = check_interfaces(router)
        print(json.dumps(interfaces, indent=2))
        interface_status.insert_one({
            "router_id": router.get("_id"),
            "ip": router.get("ip"),
            "interfaces": interfaces,
            "timestamp": datetime.now(timezone.utc),
        })
        print(f"Stored interface status for {router.get('ip')}")
    except Exception as e:
        print(f"Failed to check {router.get('ip')}: {e}")

    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

    attempt = 0
    connection = None
    while connection is None:
        print(f"Connecting to RabbitMQ (try {attempt})...")
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(RABBITMQ_HOST, credentials=credentials)
            )
        except Exception as e:
            print(f"Failed: {e}")
            attempt += 1
            time.sleep(3)

    channel = connection.channel()
    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(queue="router_jobs", exchange="jobs", routing_key="check_interfaces")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="router_jobs", on_message_callback=on_message)

    channel.start_consuming()


if __name__ == "__main__":
    main()
