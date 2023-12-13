from deephaven.appmode import ApplicationState, get_app_state
from deephaven import time_table, empty_table
from deephaven.parquet import write

from deephaven import kafka_consumer as kc
from deephaven import dtypes as dht

from typing import Callable

def start(app: ApplicationState):
  non_preprocess_table_01 = kc.consume(
    {"bootstrap.servers": "redpanda-0:9092"},
    "test_order-placement",
    key_spec=kc.KeyValueSpec.IGNORE,
    value_spec=kc.json_spec([  ('order_id', dht.string),
                               ('customer_name', dht.string),
                                ('customer_email', dht.string),
                                ('order_items', dht.string),
                                ('shipping_address', dht.string),
                                ]),
    table_type=kc.TableType.append()
    )
  app["live_order-placement"] = non_preprocess_table_01.drop_columns(cols=["KafkaPartition", "KafkaOffset"])

  non_preprocess_table_02 = kc.consume(
    {"bootstrap.servers": "redpanda-0:9092"},
    "test_shipment-tracking",
    table_type=kc.TableType.append(),
    key_spec=kc.KeyValueSpec.IGNORE,
    value_spec=kc.json_spec([  ('order_id', dht.string),
                               ('tracking_number', dht.string),
                               ('carrier', dht.string),
                               ('status', dht.string),
                               ('estimated_delivery_date', dht.string)
                               ])
    )
  app["live_shipment-tracking"] = non_preprocess_table_02.drop_columns(cols=["KafkaPartition", "KafkaOffset"])

  non_preprocess_table_03 = kc.consume(
    {"bootstrap.servers": "redpanda-0:9092"},
    "test_validate-shipment-tracking",
    table_type=kc.TableType.append(),
    key_spec=kc.KeyValueSpec.IGNORE,
    value_spec=kc.json_spec([  ('order_id', dht.string),
                               ('status', dht.string),
                               ('current_location', dht.string)
                               ])
    )
  app["live_validate-shipment-tracking"] = non_preprocess_table_03.drop_columns(cols=["KafkaPartition", "KafkaOffset"])

  non_preprocess_table_04 = kc.consume(
    {"bootstrap.servers": "redpanda-0:9092"},
    "test_KPI-analytics",
    table_type=kc.TableType.append(),
    key_spec=kc.KeyValueSpec.IGNORE,
    value_spec=kc.json_spec([  ('order_id', dht.string),
                               ('otd_percentage', dht.int_),
                               ('order_accuracy_percentage', dht.int_)])
    )
  app["live_KPI-analytics"] = non_preprocess_table_04.drop_columns(cols=["KafkaPartition", "KafkaOffset"])

def initialize(func: Callable[[ApplicationState], None]):
  app = get_app_state()
  func(app)

initialize(start)
