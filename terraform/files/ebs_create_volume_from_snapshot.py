#!/usr/bin/env python3
# coding: utf-8

from aws_library.ebs_create_volume_from_snapshot import EBSCreateVolumeFromSnapshot


def lambda_handler(event, context):
    print(f'{event["uuid"]} Creating a new volume {event["volume_type"]} '
          f'from snapshot {event["snapshot_id"]}')
    return {**event, **EBSCreateVolumeFromSnapshot(region=event['region'],
                                                   snapshot_id=event['snapshot_id'],
                                                   az=event['az'],
                                                   volume_type=event['volume_type']).start()}
