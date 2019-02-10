#!/usr/bin/env python3
# coding: utf-8

import boto3
import logging

LOGGER = logging.getLogger('ec2-cryptomatic')
LOGGER.setLevel(logging.CRITICAL)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.CRITICAL)
LOGGER.addHandler(stream_handler)


class EBSCreateSnapshot(object):
    """ Take a snapshot of an existing EBS volume """

    def __init__(self, region: str, volume_id: str, uuid: str = ''):
        self._region = region
        self._volume_id = volume_id
        self._log_base = f'{__class__.__name__} {uuid}'

        self._ec2_client = boto3.client('ec2', region_name=region)
        self._ec2_resource = boto3.resource('ec2', region_name=region)

        self._wait_snapshot = self._ec2_client.get_waiter('snapshot_completed')

        LOGGER.info(f'{self._log_base} Initializing')

    def start(self):
        """
        Take a snapshot
        :return: (dict) returns a dict with the snapshot ID
        """
        # TODO : Add an error detection of non-existing volume ID

        LOGGER.info(f'{self._log_base} Take a snapshot on EBS volume {self._volume_id}')
        volume = self._ec2_resource.Volume(self._volume_id)
        snapshot = volume.create_snapshot(Description=f'snapshot of {self._volume_id}')
        snapshot.create_tags(Tags=[{'Key': 'volume_source', 'Value': self._volume_id}])
        self._wait_snapshot.wait(SnapshotIds=[snapshot.id])

        LOGGER.info(f'{self._log_base} Snapshot created {snapshot.id}')
        return {'region': self._region,
                'volume': self._volume_id,
                'snapshot': snapshot.id}
