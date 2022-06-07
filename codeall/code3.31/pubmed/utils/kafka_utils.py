import json
import six
import logging
from kafka import KafkaProducer
from kafka import KafkaConsumer

logger = logging.getLogger(__name__)


class JsonDataProducer:
    def __init__(self, bootstrap_servers) -> None:
        # by setting batch_size and linger_ms, the producer will batch the message sending to the broker
        # the batch size should be smaller than server configured max_request_size to avoid the MESSAGE_TOO_LARGE issue
        # use flush to send message in buffer immediately
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            api_version=(0, 10),
            retries=6,
            batch_size=1048576,
            linger_ms=1000 * 2,
            max_request_size=1048576,
            key_serializer=lambda m: bytes(m, encoding="utf-8") if m else None,
            value_serializer=lambda m: bytes(
                json.dumps(m, ensure_ascii=False), encoding="utf-8"
            ),
        )

    def __del__(self):
        self.producer.close(2 * 60)
        logger.info("======= kafka json data producer closed =======")

    def send_message(self, topic: str, data: dict, id_field: str = None):
        data_id = data.get(id_field, None)
        future = self.producer.send(topic, data, key=data_id)
        future.add_callback(
            self._on_send_success, id_field=id_field, id=data_id
        ).add_errback(self._on_send_error, value=data, id_field=id_field, id=data_id)
        return future

    def close(self, timeout=2 * 60):
        self.producer.close(timeout)

    def flush(self):
        self.producer.flush()

    def _on_send_success(self, record_metadata, id_field, id):
        message = f"send kafka message success for {id_field}:{id}\tTopic:{record_metadata.topic}\tpartition:{record_metadata.partition}\toffset:{record_metadata.offset}\ttimestamp:{record_metadata.timestamp}"
        logger.debug(message)
        if record_metadata.offset % 1000 == 0:
            logger.info(message)

    def _on_send_error(self, record_metadata, value, id_field, id):
        logger.error(f"send kafka message failed for esid: {id_field}:{id}")
        logger.error(f"{record_metadata}")


class JsonDataConsumer:
    def __init__(self, bootstrap_servers, group_id, topic, subcribe=True) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topic = topic

        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            api_version=(0, 10),
            ssl_check_hostname=False,
            group_id=group_id,
            max_poll_records=10000,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            key_deserializer=lambda m: m.decode() if m else None,
            value_deserializer=lambda m: json.loads(m.decode()),
        )
        if subcribe:
            self.consumer.subscribe([self.topic])

    def topic_exist(self):
        topics = self.consumer.topics()
        return self.topic in topics

    def __del__(self):
        logger.info("======= kafka json data consumer closed =======")

    def __iter__(self):
        return self.consumer

    def pull_one_record(
        self, timeout_seconds: int, hard_commit=True, update_offsets=True
    ):
        messages = self.consumer.poll(
            timeout_ms=1000 * timeout_seconds,
            max_records=1,
            update_offsets=update_offsets,
        )
        if hard_commit:
            self.consumer.commit()
        for _, records in six.iteritems(messages):
            for record in records:
                return record

    def pull_records(
        self,
        timeout_seconds: int,
        max_records: int,
        hard_commit=True,
        update_offsets=True,
    ):
        messasges = self.consumer.poll(
            timeout_ms=1000 * timeout_seconds,
            max_records=max_records,
            update_offsets=update_offsets,
        )
        if hard_commit:
            self.consumer.commit()
        results = []
        for _, records in six.iteritems(messasges):
            results.extend(records)
        return results
