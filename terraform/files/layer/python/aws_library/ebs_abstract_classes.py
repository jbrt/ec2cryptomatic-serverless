# coding: utf-8

import abc
import boto3
import logging

LOGGER = logging.getLogger('ec2-cryptomatic')
LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
LOGGER.addHandler(stream_handler)


class LambdaBase(object, metaclass=abc.ABCMeta):
    """
    Abstract class for EBS actions
    """

    def __init__(self, region: str):
        """
        Initialization
        :param region: (str) AWS region
        """
        self._region = region
        self._log_base = f'{__class__.__name__} '

        self._ec2_client = boto3.client('ec2', region_name=region)
        self._ec2_resource = boto3.resource('ec2', region_name=region)

        LOGGER.info(f'{self._log_base} Initializing')

    def start(self):
        raise NotImplementedError
