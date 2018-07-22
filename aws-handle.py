import boto3
from datetime import datetime


class EC2Manager(object):

    def __init__(self):
        self.ec2_handler = boto3.client('ec2')
        self.reservations = self.get_reservations()

    def get_reservations(self):
        return self.ec2_handler.describe_instances().get('Reservations', [])

    def get_active_instance_count(self):
        active_counter = 0
        print self.reservations
        for reservation in self.reservations:
            instance_list = reservation.get('Instances', [])
            for instance in instance_list:
                if instance.get('State', {}).get('Name') == 'running':
                    active_counter += 1
        return active_counter

    def get_active_instance_names(self):
        active_instance_list = list()
        for reservation in self.reservations:
            instance_list = reservation.get('Instances', [])
            for instance in instance_list:
                if instance.get('State', {}).get('Name') == 'running':
                    active_instance_list.append(instance.get('Tags', [{}])[0].get('Value', ''))
        return active_instance_list

    def get_instance_id(self, server_name):
        for reservation in self.reservations:
            instance_list = reservation.get('Instances', [])
            for instance in instance_list:
                if instance.get('Tags', [{}])[0].get('Value') == server_name:
                    return instance.get('InstanceId')

    def start_server(self, server_name):
        instance_id = self.get_instance_id(server_name)
        self.ec2_handler.start_instances(InstanceIds=[instance_id])

    def stop_server(self, server_name):
        instance_id = self.get_instance_id(server_name)
        self.ec2_handler.stop_instances(InstanceIds=[instance_id])

    def get_all_server_names(self):
        instance_names = list()
        for reservation in self.reservations:
            instance_list = reservation.get('Instances', [])
            for instance in instance_list:
                instance_names.append(instance.get('Tags', [{}])[0].get('Value', ''))
        return instance_names
