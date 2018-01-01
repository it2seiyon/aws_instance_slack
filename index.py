import boto3
import json
import urllib.request
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
def handler(event, context):
    ec2client = boto3.client('ec2')
    response = ec2client.describe_instances()
    msg = ''
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["State"]["Name"] == "running":
                for key in instance["Tags"]:
                    if key["Key"] == "Name":
                        msg += "• " + key["Value"] + '\n'
    print(msg)
    send_message_to_slack(messages=msg)
                 
                        
def send_message_to_slack(url="<Replace Slack incomming url", messages=None):
    '''
    Send message to slack

    Params:
        url      : String - slack url
        messages : String - message to pass to slack
    '''
    messages=":arrows_counterclockwise: List of running instances :arrows_counterclockwise:\n"\
    +messages
    if not isinstance(messages, str):
        raise TypeError("Content must be String")

    contents = dict({'text': messages})

    data = json.dumps(contents)
    http_obj = urllib.request.urlopen(url=url, data=data.encode("utf-8"))

    print(http_obj.read())
       
