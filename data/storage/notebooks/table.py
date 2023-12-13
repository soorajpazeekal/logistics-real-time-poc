from deephaven.parquet import write, read
from deephaven.stream.kafka import consumer as kc
from deephaven import dtypes as dht


order_placement_table = kc.consume(
    {"bootstrap.servers": "redpanda-0:9092"},
    "test_order-placement",
    offsets=kc.ALL_PARTITIONS_SEEK_TO_BEGINNING,
    table_type=kc.TableType.append(),
    key_spec=kc.KeyValueSpec.IGNORE,
    value_spec=kc.json_spec([  ('order_id', dht.string),
                               ('customer_name', dht.string),
                                ('customer_email', dht.string),
                                ('order_items', dht.string),
                                ('shipping_address', dht.string),
                                ])
)


shipment_tracking_table = kc.consume(
    {"bootstrap.servers": "redpanda-0:9092"},
    "test_shipment-tracking",
    offsets=kc.ALL_PARTITIONS_SEEK_TO_BEGINNING,
    table_type=kc.TableType.append(),
    key_spec=kc.KeyValueSpec.IGNORE,
    value_spec=kc.json_spec([  ('order_id', dht.string),
                               ('tracking_number', dht.string),
                               ('carrier', dht.string),
                               ('status', dht.string),
                               ('estimated_delivery_date', dht.string)
                               ])
)


validate_shipment_tracking_table = kc.consume(
    {"bootstrap.servers": "redpanda-0:9092"},
    "test_validate-shipment-tracking",
    offsets=kc.ALL_PARTITIONS_SEEK_TO_BEGINNING,
    table_type=kc.TableType.append(),
    key_spec=kc.KeyValueSpec.IGNORE,
    value_spec=kc.json_spec([  ('order_id', dht.string),
                               ('status', dht.string),
                               ('current_location', dht.string)
                               ])
)


kpi_analytics_table = kc.consume(
    {"bootstrap.servers": "redpanda-0:9092"},
    "test_KPI-analytics",
    offsets=kc.ALL_PARTITIONS_SEEK_TO_BEGINNING,
    table_type=kc.TableType.append(),
    key_spec=kc.KeyValueSpec.IGNORE,
    value_spec=kc.json_spec([  ('order_id', dht.string),
                               ('otd_percentage', dht.int_),
                               ('order_accuracy_percentage', dht.int_)])
    )

write(order_placement_table, "my-aws-pyspark-table/order-placement/testgrades_GZIP.parquet", compression_codec_name="GZIP")
write(shipment_tracking_table, "my-aws-pyspark-table/shipment_tracking/testgrades_GZIP.parquet", compression_codec_name="GZIP")
write(validate_shipment_tracking_table, "my-aws-pyspark-table/validate_shipment/testgrades_GZIP.parquet", compression_codec_name="GZIP")
write(kpi_analytics_table, "my-aws-pyspark-table/kpi_analytics/testgrades_GZIP.parquet", compression_codec_name="GZIP")
