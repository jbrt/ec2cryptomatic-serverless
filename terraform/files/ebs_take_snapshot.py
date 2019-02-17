#!/usr/bin/env python3
# coding: utf-8

"""
Take a snapshot for a given EBS volume
"""

import boto3
from aws_library.ebs_create_snapshot import EBSCreateSnapshot


def lambda_handler(event, context):
    region = event['region']
    volume = event['volumes'][0]
    ec2 = boto3.resource('ec2', region_name=region)
    ec2volume = ec2.Volume(volume)

    if 'elements' in event:
        del event['elements']
    event['elements'] = {}

    print(f'Creating a snapshot from {volume} volume')
    return {**event, 'elements': {**event['elements'],
                                  'az': ec2volume.availability_zone,
                                  'volume_type': ec2volume.volume_type,
                                  **EBSCreateSnapshot(region=region,
                                                      volume_id=volume).start()}}
