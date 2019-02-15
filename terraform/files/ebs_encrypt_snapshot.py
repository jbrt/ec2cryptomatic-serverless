#!/usr/bin/env python3
# coding: utf-8

from aws_library.ebs_encrypt_snapshot import EBSEncryptSnapshot


def lambda_handler(event, context):
    print(f'{event["uuid"]} Encrypt snapshot event["snapshot_id"] '
          f'with event["kms_key"]')
    return {**event, **EBSEncryptSnapshot(region=event['region'],
                                          snapshot_id=event['snapshot_id'],
                                          kms_key=event['kms_key']).start()}
