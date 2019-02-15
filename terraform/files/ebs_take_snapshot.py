#!/usr/bin/env python3
# coding: utf-8

from aws_library.ebs_create_snapshot import EBSCreateSnapshot


def lambda_handler(event, context):
    print(f'{event["uuid"]} Creating a snapshot from {event["volume_id"]} volume')
    return {**event, **EBSCreateSnapshot(region=event['region'],
                                         volume_id=event['volume_id']).start()}
