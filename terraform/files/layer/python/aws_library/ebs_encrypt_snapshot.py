# coding: utf-8

import boto3
import logging

LOGGER = logging.getLogger('ec2-cryptomatic')
LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
LOGGER.addHandler(stream_handler)


class EBSEncryptSnapshot(object):
    """ Encrypt an existing EBS snapshot """

    def __init__(self, region: str, snapshot_id: str,
                 kms_key: str = 'alias/aws/ebs', uuid: str = '',
                 destroy_source=True):
        """
        Initializer
        :param region: (str) AWS region
        :param snapshot_id: (str) ID of the snapshot to encrypt
        :param kms_key: (str) KMS Key for the encryption
        :param destroy_source: (bool) if True destroy the source snapshot after encryption
        :param uuid: (str) UUID used for tracing
        """
        self._destroy_source = destroy_source
        self._region = region
        self._kms_key = kms_key
        self._snapshot_id = snapshot_id
        self._log_base = f'{__class__.__name__} {uuid}'

        self._ec2_client = boto3.client('ec2', region_name=region)
        self._ec2_resource = boto3.resource('ec2', region_name=region)

        self._wait_snapshot = self._ec2_client.get_waiter('snapshot_completed')

        LOGGER.info(f'{self._log_base} Initializing')

    def start(self):
        """
        Encrypt a snapshot
        :return: (dict) returns a dict with the snapshot ID
        """
        # TODO : Add an error detection of non-existing volume ID

        LOGGER.info(f'{self._log_base} Copy the snapshot {self._snapshot_id} '
                    f'and encrypt it ')

        snapshot = self._ec2_resource.Snapshot(self._snapshot_id)
        snap_id = snapshot.copy(Description=f'encrypted copy of {snapshot.id}',
                                Encrypted=True,
                                SourceRegion=self._region,
                                KmsKeyId=self._kms_key)
        self._wait_snapshot.wait(SnapshotIds=[snap_id['SnapshotId']])

        if self._destroy_source:
            self._ec2_resource.Snapshot(snap_id['SnapshotId']).delete()

        LOGGER.info(f'{self._log_base} Encrypted Snapshot created {snap_id["SnapshotId"]}')
        return {'region': self._region,
                'snapshot': self._snapshot_id,
                'encrypted_snapshot': snap_id['SnapshotId']}
