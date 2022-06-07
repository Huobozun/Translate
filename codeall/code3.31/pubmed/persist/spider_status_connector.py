from abc import ABC, abstractmethod
import logging
from pubmed.utils.kafka_utils import JsonDataConsumer, JsonDataProducer
from pubmed.utils.time_utils import trace_time_elapsed
from pubmed.items import PubmedArticleSetItem
from kafka import TopicPartition

logger = logging.getLogger(__name__)


class SpiderStatusConnector(ABC):
    @abstractmethod
    def get_crawled_page(self) -> list:
        pass

    @abstractmethod
    def add_crawled_page(self, file_url):
        pass


class KafkaSpiderStatusConnector(SpiderStatusConnector):
    def __init__(self, kafkahost, setting: dict):
        self.KafkaHost = kafkahost
        self.KafkaTopic = setting["KAFKA_CRAWELD_PAGE"]["KafkaTopic"]
        self.NextMainJobConsumeGroup = setting["KAFKA_CRAWELD_PAGE"][
            "NextMainJobConsumeGroup"
        ]
        self.AdditionalFieldJobGroup = setting["KAFKA_CRAWELD_PAGE"][
            "AdditionalFieldJobGroup"
        ]
        self.MaxRecords = setting["KAFKA_CRAWELD_PAGE"]["MaxPollRecords"]
        self.producer = JsonDataProducer(self.KafkaHost)
        self.full_consumer = JsonDataConsumer(
            self.KafkaHost,
            self.NextMainJobConsumeGroup,
            self.KafkaTopic,
            subcribe=False,
        )
        self.queue_consmer = JsonDataConsumer(
            self.KafkaHost, self.AdditionalFieldJobGroup, self.KafkaTopic
        )

    @trace_time_elapsed(logger=logger)
    def get_crawled_page(self):
        results = []
        partitions = self.full_consumer.consumer.partitions_for_topic(
            self.full_consumer.topic
        )
        if partitions:
            for partition in partitions:
                topic_partition = TopicPartition(self.full_consumer.topic, partition)
                self.full_consumer.consumer.assign([topic_partition])
                self.full_consumer.consumer.seek(topic_partition, 0)
                while True:
                    records = self.full_consumer.pull_records(
                        timeout_seconds=10,
                        max_records=self.MaxRecords,
                        hard_commit=False,
                        update_offsets=True,
                    )
                    if len(records) == 0:
                        break
                    results.extend(records)
        return [record.value.get("file_url", "") for record in results]

    @trace_time_elapsed(logger=logger)
    def add_crawled_page(self, item: PubmedArticleSetItem):
        self.producer.send_message(self.KafkaTopic, dict(item))
        self.producer.flush()
