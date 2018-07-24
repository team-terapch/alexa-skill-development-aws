import sys
import boto3


ec2 = boto3.client('ec2')
if sys.argv[1] == 'ON':
    response = ec2.monitor_instances(InstanceIds=['i-0dfa82e43e53d4bf7'])
else:
    response = ec2.unmonitor_instances(InstanceIds=['i-0dfa82e43e53d4bf7'])
print(response)

