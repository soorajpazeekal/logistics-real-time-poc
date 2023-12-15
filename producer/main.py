import random, json
import configparser, logging as log
from confluent_kafka import Producer, KafkaException, KafkaError

from bot import OrderPlacement, ShipmentTracking, BaseAnalytics
import time
import multiprocessing


config = configparser.ConfigParser(); config.read('.ini')
log.basicConfig(level=log.INFO)

def produce_message(**kwargs):
    """
    Produces a message to a Kafka topic.

    Args:
        **kwargs: Keyword arguments.
            producer_config (dict): The configuration for the Kafka producer.
            value_as_json (str): The JSON string representation of the message value.
            Topic (str): The Kafka topic to produce the message to.

    Raises:
        KafkaException: If there is an error while producing the message.
            - If the message delivery times out, a KafkaError._MSG_TIMED_OUT exception is raised.
            - If the topic or partition does not exist or is unavailable, a KafkaError.UNKNOWN_TOPIC_OR_PART exception is raised.

    Returns:
        None
    """
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
    """
    Executes the main function.

    This function runs an infinite loop and performs the following steps:
    1. Configures the producer with the specified bootstrap servers and compression type.
    2. Generates order placement data using the `generate_order_placement_data` function.
    3. Converts the order placement data to JSON format.
    4. Waits for a random number of seconds between 10 and 60.
    5. Produces a message to the "test_order-placement" topic using the specified producer configuration and JSON value.
    6. Converts the JSON value back to a dictionary.
    7. Generates shipment tracking data using the order ID and shipping address from the JSON value.
    8. Converts the shipment tracking data to JSON format.
    9. Waits for a random number of seconds between 10 and 60.
    10. Produces a message to the "test_shipment-tracking" topic using the specified producer configuration and JSON value.
    11. Converts the JSON value back to a dictionary.
    12. Validates the shipment tracking data using the order ID, status, and estimated delivery date from the JSON value.
    13. Converts the validation result to JSON format.
    14. Waits for a random number of seconds between 10 and 60.
    15. Produces a message to the "test_validate-shipment-tracking" topic using the specified producer configuration and JSON value.
    16. Converts the JSON value back to a dictionary.
    17. Calculates the KPI metrics for on-time delivery using the order ID from the JSON value.
    18. Converts the KPI metrics to JSON format.
    19. Produces a message to the "test_KPI-analytics" topic using the specified producer configuration and JSON value.
    """
    while True:
        producer_config = {
            'bootstrap.servers': config['DEFAULT']['docker_bootstrap_servers'],
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
