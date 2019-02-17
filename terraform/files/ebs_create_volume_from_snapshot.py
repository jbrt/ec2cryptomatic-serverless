#!/usr/bin/env python3
# coding: utf-8

"""
Create a brand new volume from a given snapshot
"""

from aws_library.ebs_create_volume_from_snapshot import EBSCreateVolumeFromSnapshot


def lambda_handler(event, context):
    region = event['region']
    snapshot_id = event['elements']['encrypted_snapshot_id']
    az = event['elements']['az']
    volume_type = event['elements']['volume_type']

    print(f'Creating a new volume {volume_type} from snapshot {snapshot_id}')
    return {**event, 'elements': {**event['elements'],
                                  **EBSCreateVolumeFromSnapshot(region=region,
                                                                snapshot_id=snapshot_id,
                                                                az=az,
                                                                volume_type=volume_type).start()}}
