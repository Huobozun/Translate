import logging
from pubmed.utils.serialize_utils import JsonSerializer
from pubmed.utils.kafka_utils import JsonDataProducer
from pubmed.utils.time_utils import trace_time_elapsed

logger = logging.getLogger(__name__)


class KafkaToEsConnector:
    def __init__(self, kafkahost, setting: dict):
        self.KafkaHost = kafkahost
        self.KafkaTopic = setting["KAFKA_TO_ES"]["KafkaTopic"]
        self.EsIndex = setting["KAFKA_TO_ES"]["EsIndex"]
        self.producer = JsonDataProducer(self.KafkaHost)

    @trace_time_elapsed(logger=logger)
    def send_message_from_file(self, file_path: str, esid_field="pmid"):
        df = JsonSerializer.deserilize_records_from_file(file_path)
        logger.info(f"data pending send to kafka count = {len(df.index)}")
        for _, row in df.iterrows():
            data_dict = row.to_dict()
            self.send_message(data_dict, esid_field=esid_field)
        self.producer.flush()

    def close(self, timeout=2 * 60):
        self.producer.close(timeout=timeout)

    def send_message_batch(self, data: list, esid_field="pmid"):
        logger.info(f"data pending send to kafka count = {len(data)}")
        for row in data:
            data_dict = row
            self.send_message(data_dict, esid_field=esid_field)
        self.producer.flush()

    def send_message(self, data: dict, esid_field="pmid", do_flush=False):
        esid = data[esid_field]
        kafka_dict = {}
        kafka_dict["esid"] = esid
        kafka_dict["list"] = [data]
        kafka_dict["index_name"] = self.EsIndex
        kafka_dict["operate"] = "insert_or_update_fields"
        future = self.producer.send_message(
            self.KafkaTopic, kafka_dict, id_field="esid"
        )
        if do_flush:
            self.producer.flush()
        return future
