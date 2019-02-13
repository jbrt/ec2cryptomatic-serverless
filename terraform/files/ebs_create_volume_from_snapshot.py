#!/usr/bin/env python3
# coding: utf-8

from aws_library.ebs_create_volume_from_snapshot import EBSCreateVolumeFromSnapshot


def lambda_handler(event, context):
    EBSCreateVolumeFromSnapshot(region=event['region'],
                                snapshot_id=event['snapshot_id'],
                                az=event['az'],
                                volume_type=event['volume_type'],
                                uuid=event['event']).start()
