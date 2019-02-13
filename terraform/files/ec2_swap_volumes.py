#!/usr/bin/env python3
# coding: utf-8

from aws_library.ec2_swap_volumes import EC2SwapVolumes


def lambda_handler(event, context):
    EC2SwapVolumes(region=event['region'],
                   instance_id=event['instance_id'],
                   volume=event['volume'],
                   new_volume=event['new_volume'],
                   uuid=event['uuid']).start()
