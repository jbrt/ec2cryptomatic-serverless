#!/usr/bin/env python3
# coding: utf-8

"""
Encrypt a given snapshot (by copying a non-encrypted snapshot)
"""

from aws_library.ebs_encrypt_snapshot import EBSEncryptSnapshot


def lambda_handler(event, context):
    region = event['region']
    snapshot_id = event['elements']['snapshot_id']
    kms_key = event['kms_key']

    print(f'Encrypt snapshot event["snapshot_id"] with event["kms_key"]')
    return {**event, 'elements': {**event['elements'],
                                  **EBSEncryptSnapshot(region=region,
                                                       snapshot_id=snapshot_id,
                                                       kms_key=kms_key).start()}}
