# coding: utf-8

"""
Delete the encrypted and the EBS source volume (if delete_source == True)
"""


import boto3


def lambda_handler(event, context):
    region = event['region']
    snapshot_id = event['elements']['encrypted_snapshot_id']
    delete_source = event['delete_source']
    volume_id = event['volumes'][0]
    ec2 = boto3.resource('ec2', region_name=region)

    # First we delete the encrypted snapshot used for the
    # creation of the encrypted volume
    snapshot = ec2.Snapshot(id=snapshot_id)
    print(f'Delete the encrypted snapshot {snapshot_id}')
    snapshot.delete()

    # Then, if the user as specified to delete_source flag, delete
    # the original EBS volume
    if delete_source:
        print(f'Delete_source flag is True so, deleting source '
              f'volume {volume_id}')
        volume = ec2.Volume(id=volume_id)
        volume.delete()

    # Finally, delete the volume from the volume list in the event structure
    event['volumes'].pop(0)
    if not event['volumes']:
        event['has_elements'] = False

    return event
