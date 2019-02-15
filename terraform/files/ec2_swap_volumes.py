#!/usr/bin/env python3
# coding: utf-8

from aws_library.ec2_swap_volumes import EC2SwapVolumes


def lambda_handler(event, context):
    print(f'{event["uuid"]} Swap volume {event["volume"]} by '
          f'{event["new_volume"]} for instance {event["instance_id"]}')
    return {**event, **EC2SwapVolumes(region=event['region'],
                                      instance_id=event['instance_id'],
                                      volume=event['volume'],
                                      new_volume=event['new_volume']).start()}
