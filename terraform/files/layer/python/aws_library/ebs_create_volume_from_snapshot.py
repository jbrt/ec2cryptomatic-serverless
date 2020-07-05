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


class EBSCreateVolumeFromSnapshot(LambdaBase):

    def __init__(self, region: str, az: str, snapshot_id: str, volume_type: str):
        """
        Initialization
        :param region: (str) AWS region
        :param az: (str) AWS AZ (ex: gp2)
        :param snapshot_id: (str) ID of the snapshot
        :param volume_type: (str) type of the EBS volume
        """
        super().__init__(region=region)

        self._az = az
        self._snapshot_id = snapshot_id
        self._volume_type = volume_type
        self._wait_volume = self._ec2_client.get_waiter('volume_available')
        self._wait_volume.config.max_attempts = MAX_RETRIES
        self._wait_volume.config.delay = DELAY_RETRY

    def start(self):
        LOGGER.info(f'Create a new EBS {self._volume_type} volume '
                    f'from {self._snapshot_id}')
        snapshot = self._ec2_resource.Snapshot(self._snapshot_id) 
        volume = self._ec2_resource.create_volume(SnapshotId=snapshot.id,
                                                  VolumeType=self._volume_type,
                                                  TagSpecifications=[
                                          {
                                           'ResourceType': 'volume',
                                           'Tags': snapshot.tags
                                          },
                                 ],
                                                  AvailabilityZone=self._az)
        self._wait_volume.wait(VolumeIds=[volume.id])
        return {'new_volume': volume.id}
