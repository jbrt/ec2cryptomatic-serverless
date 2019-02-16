# coding: utf-8

import boto3


def lambda_handler(event, context):
    region = event['region']
    snapshot_id = event['elements']['encrypted_snapshot_id']
    ec2 = boto3.resource('ec2', region_name=region)

    snapshot = ec2.Snapshot(id=snapshot_id)
    print(f'Delete the encrypted snapshot {snapshot_id}')
    snapshot.delete()

    return event
