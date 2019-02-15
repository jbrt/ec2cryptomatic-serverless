#!/usr/bin/env python3
# coding: utf-8

from aws_library.ebs_create_snapshot import EBSCreateSnapshot


def lambda_handler(event, context):
    return EBSCreateSnapshot(region=event['region'],
                             volume_id=event['volume_id'],
                             uuid=event['uuid']).start()
