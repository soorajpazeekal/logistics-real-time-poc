from faker import Faker
import json
import random, logging as log
from datetime import datetime, timedelta

import time

fake = Faker()
log.basicConfig(level=log.INFO)


class OrderPlacement:
    def generate_order_placement_data():
        """
        Generates order placement data.

        :return: dict -- A dictionary containing order placement data.
        """
        order_data = {
            "order_id": fake.uuid4(),
            "customer_name": fake.name(),
            "customer_email": fake.email(),
            "order_date": datetime.now(),
            "order_items": OrderPlacement.generate_random_products(),
            "shipping_address": OrderPlacement.generate_shipping_address(),
        }
        return order_data
    
    def generate_random_products():
        """
        Generates a list of random products.
        
        Returns:
            list: A list of dictionaries, where each dictionary represents a product.
                Each product dictionary contains the following keys:
                - "product_id" (str): The unique identifier for the product.
                - "product_name" (str): The name of the product.
                - "quantity" (int): The quantity of the product.
                - "price" (float): The price of the product.
        """
        num_products = random.randint(1, 5); products = []
        for _ in range(num_products):
            product = {
                "product_id": fake.uuid4(),
                "product_name": fake.word(),
                "quantity": random.randint(1, 10),
                "price": float(fake.random_int(10, 100))
            }
            products.append(product)
        return products
    
    def generate_shipping_address():
        return {
        "address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "zip_code": fake.zipcode()}
    
class ShipmentTracking:
    def generate_shipment_tracking_data(order_id, shipping_address):
        """
        Generates shipment tracking data for an order.

        Parameters:
            order_id (int): The ID of the order.
            shipping_address (str): The address to which the shipment is being sent.

        Returns:
            dict: A dictionary containing the shipment tracking data, including the order ID, tracking number, carrier,
                  estimated delivery date, status, and shipping address.
        """
        status_choices = ["Shipped"] * 7 + ["User Cancelled"] * 3
        shipment_data = {
            "order_id": order_id,
            "tracking_number": fake.uuid4(),
            "carrier": fake.random_element(elements=("UPS", "FedEx", "DHL")),
            "estimated_delivery_date": datetime.now() + timedelta(minutes = random.randint(10, 60)),
            "status": random.choice(status_choices),
            "shipping_address": shipping_address
        }
        return shipment_data
    def validate_shipment_tracking_data(order_id, status, estimated_delivery_date):
            """
            Validates the shipment tracking data based on the given order ID, status, and estimated delivery date.

            Args:
                order_id (int): The unique identifier of the order.
                status (str): The current status of the shipment.
                estimated_delivery_date (str): The estimated delivery date of the shipment.

            Returns:
                dict: A dictionary representing the validated shipment tracking data. The dictionary contains the following keys:
                    - order_id (int): The unique identifier of the order.
                    - status (str): The current status of the shipment.
                    - current_location (dict): A dictionary representing the current location of the shipment. The dictionary contains the following keys:
                        - latitude (float): The latitude of the current location.
                        - longitude (float): The longitude of the current location.
                    - estimated_delivery_date (str): The estimated delivery date of the shipment.
            """
            if status == "Shipped":
                status_choices = ["In Transit"] * 4 + ["Out for Delivery"] * 3 + ["Delivered"] * 3
                tracking_data = {
                    "order_id": order_id,
                    "status": random.choice(status_choices),
                    "current_location": {
                        "latitude":  random.random() * 0.5 + 39.8,
                        "longitude": random.random() * 0.5 - 75.2
                    },
                    "estimated_delivery_date": estimated_delivery_date
                    }
                return tracking_data
            else:
                return {
                    "order_id": order_id,
                    "status": status
                }
            
class BaseAnalytics:
    def on_time_delivery(order_id):
        """
        Generate a final analytics report for a given order.

        Args:
            order_id (int): The ID of the order.

        Returns:
            dict: A dictionary containing the order ID, time stamp, on-time delivery percentage, and order accuracy percentage.
        """
        final_analytics = {
            "order_id": order_id,
            "time_stamp": datetime.now(),
            "otd_percentage": random.randint(10, 100),
            "order_accuracy_percentage": random.randint(80, 99)
        }
        return final_analytics

        

def main_flow():
    while True:
        order_placement_data = OrderPlacement.generate_order_placement_data()
        value_as_json = json.dumps(order_placement_data, default=str)
        value_as_json = json.loads(value_as_json)
        log.info(f"Order Placement: {value_as_json}")
        value_as_json = ShipmentTracking.generate_shipment_tracking_data(value_as_json["order_id"], value_as_json["shipping_address"])
        log.info(f"Shipment Tracking: {value_as_json}")
        time.sleep(5)
        value_as_json = ShipmentTracking.validate_shipment_tracking_data(value_as_json["order_id"], value_as_json["status"], value_as_json["estimated_delivery_date"])
        log.info(f"Shipment validation Tracking: {value_as_json}")
        value_as_json = BaseAnalytics.on_time_delivery(value_as_json["order_id"])
        log.info(f"Base Analytics: {value_as_json}")


if __name__ == "__main__":
    main_flow()