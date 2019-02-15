#!/usr/bin/env python3
# coding: utf-8

from aws_library.ebs_encrypt_snapshot import EBSEncryptSnapshot


def lambda_handler(event, context):
    return EBSEncryptSnapshot(region=event['region'],
                              snapshot_id=event['snapshot_id'],
                              kms_key=event['kms_key']).start()
