#!/usr/bin/env python3

import boto3
from requests import get
from os import getenv
from json import loads

from flask import Flask
app = Flask(__name__)

SAMPLE_RESPONSE = {
    "Cluster": "arn:aws:ecs:us-west-2:&ExampleAWSAccountNo1;:cluster/default",
    "TaskARN": "arn:aws:ecs:us-west-2:333258026273:task/0dcc1dd4-8872-4599-bb15-e1ca88844ead",
    "Family": "query-metadata",
    "Revision": "7",
    "DesiredStatus": "RUNNING",
    "KnownStatus": "RUNNING",
    "Limits": {
        "CPU": 0.25,
        "Memory": 512
    },
    "PullStartedAt": "2020-03-26T22:25:40.420726088Z",
    "PullStoppedAt": "2020-03-26T22:26:22.235177616Z",
    "AvailabilityZone": "us-west-2c",
    "Containers": [
        {
            "DockerId": "febee046097849aba589d4435207c04aquery-metadata",
            "Name": "query-metadata",
            "DockerName": "query-metadata",
            "Image": "mreferre/eksutils",
            "ImageID": "sha256:1b146e73f801617610dcb00441c6423e7c85a7583dd4a65ed1be03cb0e123311",
            "Labels": {
                "com.amazonaws.ecs.cluster": "arn:aws:ecs:us-west-2:&ExampleAWSAccountNo1;:cluster/default",
                "com.amazonaws.ecs.container-name": "query-metadata",
                "com.amazonaws.ecs.task-arn": "arn:aws:ecs:us-west-2:&ExampleAWSAccountNo1;:task/default/febee046097849aba589d4435207c04a",
                "com.amazonaws.ecs.task-definition-family": "query-metadata",
                "com.amazonaws.ecs.task-definition-version": "7"
            },
            "DesiredStatus": "RUNNING",
            "KnownStatus": "RUNNING",
            "Limits": {
                "CPU": 2
            },
            "CreatedAt": "2020-03-26T22:26:24.534553758Z",
            "StartedAt": "2020-03-26T22:26:24.534553758Z",
            "Type": "NORMAL",
            "Networks": [
                {
                    "NetworkMode": "awsvpc",
                    "IPv4Addresses": [
                        "10.0.0.108"
                    ],
                    "AttachmentIndex": 0,
                    "IPv4SubnetCIDRBlock": "10.0.0.0/24",
                    "MACAddress": "0a:62:17:7a:36:68",
                    "DomainNameServers": [
                        "10.0.0.2"
                    ],
                    "DomainNameSearchList": [
                        "us-west-2.compute.internal"
                    ],
                    "PrivateDNSName": "ip-10-0-0-108.us-west-2.compute.internal",
                    "SubnetGatewayIpv4Address": ""
                }
            ]
        }
    ]
}

def get_container_arn():
    if getenv('TESTING'):
        return SAMPLE_RESPONSE['TaskARN']
    else:
        return loads(get(getenv('ECS_CONTAINER_METADATA_URI_V4')).text)['TaskARN']
    

@app.route('/')
def print_tasks_cap_prov_strategy():
    c = boto3.client('ecs')
    arns = c.list_tasks(cluster='container-demo')['taskArns']
    print(arns)
    all_tasks = c.describe_tasks(cluster='container-demo', tasks=arns)['tasks']
    print(all_tasks)
    results = {x['taskArn']: x['capacityProviderName'] for x in all_tasks}
    my_arn = get_container_arn()
    my_strategy = results[my_arn]
    final_json = {
        'MY_ARN': my_arn,
        'MY_STRATEGY': my_strategy,
        'ALL_TASKS': results
    }
    return final_json
