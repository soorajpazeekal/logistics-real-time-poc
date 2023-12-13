from deephaven.appmode import ApplicationState
from deephaven.parquet import write
from deephaven.stream.kafka import consumer as kc
from deephaven import dtypes as dht

def start(app: ApplicationState):
    result_append = kc.consume(
        {"bootstrap.servers": "redpanda-0:9092"},
        "test_order-placement",
        offsets=kc.ALL_PARTITIONS_SEEK_TO_BEGINNING,
        table_type=kc.TableType.append(),
        key_spec=kc.KeyValueSpec.IGNORE,
        value_spec=kc.simple_spec("Command", dht.string)
        )

initialize(start)