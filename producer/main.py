import random, json
import configparser, logging as log
from confluent_kafka import Producer, KafkaException, KafkaError

from bot import OrderPlacement, ShipmentTracking, BaseAnalytics
import time
import multiprocessing


config = configparser.ConfigParser(); config.read('.ini')
log.basicConfig(level=log.INFO)

def produce_message(**kwargs):
    producer = Producer(kwargs['producer_config']); value_as_json = kwargs['value_as_json']; 
    Topic = kwargs['Topic']; value_as_bytes = value_as_json.encode('utf-8')
    value_as_json = json.loads(value_as_json)
    try:
        producer.produce(Topic, key=value_as_json['order_id'], value=value_as_bytes)
        producer.flush()
        log.info("Message Written to Topic")
    except KafkaException as e:
        if e.args[0].code() == KafkaError._MSG_TIMED_OUT:
            log.error("Message delivery timed out")
        elif e.args[0].code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
            log.error("Topic or partition does not exist or unavailable")
        else:
            log.error(e)


def main():
    while True:
        producer_config = {
            'bootstrap.servers': config['DEFAULT']['bootstrap_servers'],
            'compression.type': "snappy",
            }
        order_placement_data = OrderPlacement.generate_order_placement_data()
        value_as_json = json.dumps(order_placement_data, default=str)
        time.sleep(random.randint(10, 60))
        produce_message(Topic="test_order-placement", producer_config=producer_config, value_as_json=value_as_json)
        value_as_json = json.loads(value_as_json)
        ShipmentTracking_data = ShipmentTracking.generate_shipment_tracking_data(value_as_json["order_id"], value_as_json["shipping_address"])
        value_as_json = json.dumps(ShipmentTracking_data, default=str)
        time.sleep(random.randint(10, 60))
        produce_message(Topic="test_shipment-tracking", producer_config=producer_config, value_as_json=value_as_json)
        value_as_json = json.loads(value_as_json)
        validate_shipment_tracking_data = ShipmentTracking.validate_shipment_tracking_data(value_as_json["order_id"], value_as_json["status"], value_as_json["estimated_delivery_date"])
        value_as_json = json.dumps(validate_shipment_tracking_data, default=str)
        time.sleep(random.randint(10, 60))
        produce_message(Topic="test_validate-shipment-tracking", producer_config=producer_config, value_as_json=value_as_json)
        value_as_json = json.loads(value_as_json)
        kpi_metrics = BaseAnalytics.on_time_delivery(value_as_json["order_id"])
        value_as_json = json.dumps(kpi_metrics, default=str)
        produce_message(Topic="test_KPI-analytics", producer_config=producer_config, value_as_json=value_as_json)


if __name__ == "__main__":

    processes = []
    for _ in range(5):
        try:
            process = multiprocessing.Process(target=main)
            processes.append(process)
            process.start()
            log.info(f"Process {process.pid} started")
        except KeyboardInterrupt:
            for process in processes:
                process.terminate()
                log.info(f"Process {process.pid} terminated")
