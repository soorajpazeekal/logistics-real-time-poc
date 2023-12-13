import __init__, json
import unittest

from bot import OrderPlacement, ShipmentTracking, BaseAnalytics


class TestGenerateJsonData(unittest.TestCase):
    def test_generate_json_data(self):
        order_placement_data = OrderPlacement.generate_order_placement_data()
        value_as_json = json.dumps(order_placement_data, default=str)
        self.assertIsInstance(value_as_json, str)
    def test_generate_shipment_tracking_data(self):
        order_placement_data = OrderPlacement.generate_order_placement_data()
        value_as_json = json.dumps(order_placement_data, default=str)
        value_as_json = json.loads(value_as_json)
        value_as_json = ShipmentTracking.generate_shipment_tracking_data(value_as_json["order_id"], value_as_json["shipping_address"])
        value_as_json = json.dumps(order_placement_data, default=str)
        self.assertIsInstance(value_as_json, str)
    def test_generate_shipment_kpi(self):
        value_as_json = BaseAnalytics.on_time_delivery("9139824e-0136-4e1b-8023-0fd2bbf5e1d4")
        self.assertIsInstance(value_as_json, dict)


if __name__ == '__main__':
    unittest.main()


