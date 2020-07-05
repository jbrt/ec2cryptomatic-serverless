# coding: utf-8

import logging
from aws_library.ebs_abstract_classes import LambdaBase

LOGGER = logging.getLogger('ec2-cryptomatic')
LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
LOGGER.addHandler(stream_handler)

# Constants
MAX_RETRIES = 360
DELAY_RETRY = 30


class EBSCreateSnapshot(LambdaBase):
    """ Take a snapshot of an existing EBS volume """

    def __init__(self, region: str, volume_id: str):
        """
        Initializer
        :param region: (str) AWS region (ex: eu-west-1)
        :param volume_id: (str) EBS volume ID
        """
        super().__init__(region=region)

        self._volume_id = volume_id
        self._wait_snapshot = self._ec2_client.get_waiter('snapshot_completed')
        self._wait_snapshot.config.max_attempts = MAX_RETRIES
        self._wait_snapshot.config.delay = DELAY_RETRY

    def start(self):
        """
        Take a snapshot
        :return: (dict) returns a dict with the snapshot ID
        """
        LOGGER.info(f'{self._log_base} Take a snapshot on EBS volume {self._volume_id}')
        volume = self._ec2_resource.Volume(self._volume_id)
        #snapshot = volume.create_snapshot(Description=f'snapshot of {self._volume_id}')
        #-snapshot.create_tags(Tags=[{'Key': 'volume_source', 'Value': self._volume_id}])
        snapshot = volume.create_snapshot(Description=f'snapshot of {self._volume_id}',
                                          TagSpecifications=[
                                            {
                                              'ResourceType': 'snapshot',
                                              'Tags': volume.tags
                                            },
                                          ]
                   )
        self._wait_snapshot.wait(SnapshotIds=[snapshot.id])

        LOGGER.info(f'{self._log_base} Snapshot created {snapshot.id}')
        return {'snapshot_id': snapshot.id}
