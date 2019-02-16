# coding: utf-8

import logging
from aws_library.ebs_abstract_classes import LambdaBase

LOGGER = logging.getLogger('ec2-cryptomatic')
LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
LOGGER.addHandler(stream_handler)


class EC2SwapVolumes(LambdaBase):

    def __init__(self, region: str, instance_id: str, volume: str, new_volume: str):
        """
        Initialization
        :param region: (str) AWS region
        :param instance_id: (str) Instance ID
        :param volume: (str) volume ID to bo swapped
        :param new_volume: (str) new volume to use
        """
        super().__init__(region=region)
        self._instance_id = instance_id
        self._volume = volume
        self._new_volume = new_volume
        self._wait_volume = self._ec2_client.get_waiter('volume_available')

    def start(self):
        LOGGER.info(f'For instance {self._instance_id} swap volume '
                    f'{self._volume} by {self._new_volume}')

        instance = self._ec2_resource.Instance(self._instance_id)
        volume = self._ec2_resource.Volume(self._volume)
        new_volume = self._ec2_resource.Volume(self._new_volume)

        # Adding tags on the new volume from the original one
        new_volume.create_tags(Tags=volume.tags)

        # Extract device name (ex: /dev/xvda) and DeleteOnTermination flag
        device = volume.attachments[0]['Device']
        flag = volume.attachments[0]['DeleteOnTermination']

        instance.detach_volume(Device=device, VolumeId=self._volume)
        self._wait_volume.wait(VolumeIds=[self._volume])

        instance.attach_volume(Device=device, VolumeId=self._new_volume)
        instance.modify_attribute(BlockDeviceMappings=[{'DeviceName': device,
                                                        'Ebs': {'DeleteOnTermination':  flag}}])
