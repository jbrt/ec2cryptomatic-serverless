# coding: utf-8

"""
Extract the EBS volumes from the given instance
"""

import boto3
import logging

LOGGER = logging.getLogger('ec2-cryptomatic')
LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
LOGGER.addHandler(stream_handler)


def lambda_handler(event, context):
    instance_id = event['instance_id']
    region = event['region']

    volumes = []

    ec2 = boto3.resource('ec2', region_name=region)
    instance = ec2.Instance(id=instance_id)

    for device in instance.block_device_mappings:
        if 'Ebs' not in device:
            msg = f'{instance_id} Skip {device["VolumeId"]} not an EBS device'
            LOGGER.warning(msg)
            continue
        # If the volume is an EBS volume, add it to the volume list
        volumes.append(device['Ebs']['VolumeId'])

    for device in instance.volumes.all():
        # If the volume is already encrypted we skip it and delete it
        # from the volume list
        if device.id in volumes and device.encrypted:
            msg = f'{instance_id} Volume {device.io} already encrypted'
            LOGGER.warning(msg)
            del volumes[device.id]
            continue

    return {**event,
            'volumes': volumes,
            'has_elements': True if volumes else False}
