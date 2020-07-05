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


class EBSEncryptSnapshot(LambdaBase):
    """ Encrypt an existing EBS snapshot """

    def __init__(self, region: str, snapshot_id: str, kms_key: str = 'alias/aws/ebs'):
        """
        Initializer
        :param region: (str) AWS region
        :param snapshot_id: (str) ID of the snapshot to encrypt
        :param kms_key: (str) KMS Key for the encryption
        """
        super().__init__(region=region)

        self._kms_key = kms_key
        self._snapshot_id = snapshot_id
        self._wait_snapshot = self._ec2_client.get_waiter('snapshot_completed')
        self._wait_snapshot.config.max_attempts = MAX_RETRIES
        self._wait_snapshot.config.delay = DELAY_RETRY

    def start(self):
        """
        Encrypt a snapshot
        :return: (dict) returns a dict with the snapshot ID
        """
        LOGGER.info(f'{self._log_base} Copy the snapshot {self._snapshot_id} '
                    f'and encrypt it ')

        snapshot = self._ec2_resource.Snapshot(self._snapshot_id)
        snap_id = snapshot.copy(Description=f'encrypted copy of {snapshot.id}',
                                Encrypted=True,
                                TagSpecifications=[
                                          {
                                           'ResourceType': 'snapshot',
                                           'Tags': snapshot.tags
                                          },
                                 ],
                                SourceRegion=self._region,
                                KmsKeyId=self._kms_key)
        self._wait_snapshot.wait(SnapshotIds=[snap_id['SnapshotId']])

        # Delete the original snapshot after encryption
        self._ec2_resource.Snapshot(self._snapshot_id).delete()

        LOGGER.info(f'{self._log_base} Encrypted Snapshot created {snap_id["SnapshotId"]}')
        return {'encrypted_snapshot_id': snap_id['SnapshotId']}
