#!/usr/bin/env python3
# coding: utf-8

"""
Check the given instance if suitable for conversion
"""

import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import EndpointConnectionError


class InstanceNotSuitable(Exception):
    """
    If something goes wrong this exception will stop the machine
    """
    pass


def lambda_handler(event, context):
    region = event['region']
    instance_id = event['instance_id']
    ec2_client = boto3.client('ec2', region_name=region)
    ec2_resource = boto3.resource('ec2', region_name=region)

    try:
        # Is the instance is in the good state (or exists) ?
        # If not, raise exception
        ec2_client.describe_instances(InstanceIds=[instance_id])
        instance = ec2_resource.Instance(id=instance_id)
        if instance.state['Name'] != 'stopped':
            raise TypeError(f'Instance {instance_id} not stopped ! please stop it.')

    except (EndpointConnectionError, ValueError) as error:
        raise InstanceNotSuitable(f'Problem with your AWS region ? ({error})')

    except (ClientError, TypeError) as error:
        raise InstanceNotSuitable(f'Problem with the instance ({error})')
    else:
        return event
