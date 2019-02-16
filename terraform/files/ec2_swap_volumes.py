#!/usr/bin/env python3
# coding: utf-8

from aws_library.ec2_swap_volumes import EC2SwapVolumes


def lambda_handler(event, context):
    region = event['region']
    volume = event['volumes'][0]
    new_volume = event['elements']['new_volume']
    instance_id = event['instance_id']

    print(f'Swap volume {volume} by {new_volume} for instance {instance_id}')
    EC2SwapVolumes(region=region,
                   instance_id=instance_id,
                   volume=volume,
                   new_volume=new_volume).start()

    # Delete the volume
    event['volumes'].pop(0)
    if not event['volumes']:
        event['has_elements'] = False

    return event
