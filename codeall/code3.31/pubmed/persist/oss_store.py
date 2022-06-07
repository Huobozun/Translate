import os
import oss2
import logging
from pubmed.persist.store import Store


"""
*阿里云oss系统：https://help.aliyun.com/document_detail/88435.html
* 外网地址，：http://oss-cn-beijing.aliyuncs.com
* 内网地址，：http://oss-cn-beijing-internal.aliyuncs.com
"""
logger = logging.getLogger(__name__)


class OssStore(Store):
    def __init__(self, setting: dict):
        self.Endpoint = setting["OSS_STORE"]["Endpoint"]
        self.Bucket = setting["OSS_STORE"]["Bucket"]
        self.AccessKeyId = setting["OSS_STORE"]["AccessKeyId"]
        self.AccessKeySecret = setting["OSS_STORE"]["AccessKeySecret"]
        self.oss_bucket, self.oss_bucket_info = self._collect()
        self.root_path = (
            f"https://{self.Bucket}.{self.oss_bucket_info.extranet_endpoint}"
        )

    def _collect(self):
        oss2.set_stream_logger("oss2", logging.WARNING)
        logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

        bucket = oss2.Bucket(
            oss2.Auth(self.AccessKeyId, self.AccessKeySecret),
            self.Endpoint,
            self.Bucket,
        )
        bucket_info = bucket.get_bucket_info()
        logger.info("name: " + bucket_info.name)
        logger.info("storage class: " + bucket_info.storage_class)
        logger.info("creation date: " + bucket_info.creation_date)
        logger.info("intranet_endpoint: " + bucket_info.intranet_endpoint)
        logger.info("extranet_endpoint " + bucket_info.extranet_endpoint)
        logger.info("owner: " + bucket_info.owner.id)
        logger.info("grant: " + bucket_info.acl.grant)
        logger.info("data_redundancy_type:" + bucket_info.data_redundancy_type)
        bucket.put_object
        return bucket, bucket_info

    def save(self, file_name, data, overwite=True) -> str:
        if not overwite and self.oss_bucket.object_exists(file_name):
            return
        result = self.oss_bucket.put_object(file_name, data)
        if result.status == 200:
            return os.path.join(self.root_path, file_name)
        else:
            self.logger.info(f"failed to save {file_name} using {__class__}")
            return ""

    def append(self, file_name, data):
        result = self.oss_bucket.append_object(file_name, data)
        if result.status == 200:
            return os.path.join(self.root_path, file_name)
        else:
            logger.info(f"failed to save {file_name} using {__class__}")
            return ""

    def clean(self, file_name):
        if self.oss_bucket.object_exists(file_name):
            self.oss_bucket.delete_object(file_name)
        return os.path.join(self.root_path, file_name)

    def file_exists(self, file_name) -> bool:
        return self.oss_bucket.object_exists(file_name)

    def full_path(self, file_name) -> bool:
        return os.path.join(self.root_path, file_name)
