# coding: utf-8

import logging
from aws_library.ebs_abstract_classes import LambdaBase

LOGGER = logging.getLogger('ec2-cryptomatic')
LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
LOGGER.addHandler(stream_handler)


class EBSCreateSnapshot(LambdaBase):
    """ Take a snapshot of an existing EBS volume """

    def __init__(self, region: str, volume_id: str, delete_source: True):
        """
        Initializer
        :param region: (str) AWS region (ex: eu-west-1)
        :param volume_id: (str) EBS volume ID
        :param delete_source: (bool) Delete the source volume if True
        """
        super().__init__(region=region)

        self._delete_source = delete_source
        self._volume_id = volume_id
        self._wait_snapshot = self._ec2_client.get_waiter('snapshot_completed')
        self._wait_volume = self._ec2_client.get_waiter('volume_available')

    def start(self):
        """
        Take a snapshot
        :return: (dict) returns a dict with the snapshot ID
        """
        LOGGER.info(f'{self._log_base} Take a snapshot on EBS volume {self._volume_id}')
        volume = self._ec2_resource.Volume(self._volume_id)
        snapshot = volume.create_snapshot(Description=f'snapshot of {self._volume_id}')
        snapshot.create_tags(Tags=[{'Key': 'volume_source', 'Value': self._volume_id}])
        self._wait_snapshot.wait(SnapshotIds=[snapshot.id])

        if self._delete_source:
            LOGGER.info(f'Deleting source volume {self._volume_id}')
            device = volume.attachments[0]['Device']
            instance = self._ec2_resource.Instance(id=volume.attachments[0]['InstanceId'])
            instance.detach_volume(Device=device, VolumeId=volume.id)
            self._wait_volume.wait(VolumeIds=volume.id)
            volume.delete()

        LOGGER.info(f'{self._log_base} Snapshot created {snapshot.id}')
        return {'snapshot_id': snapshot.id}
