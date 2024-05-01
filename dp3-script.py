#!/home/gitpod/.pyenv/shims/python3

import boto3
from botocore.exceptions import ClientError
import requests
import json
import collections
from collections import OrderedDict

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/ktq3td"
sqs = boto3.client('sqs', region_name='us-east-1')

# Storing all of the messages in the queue
AllMessages = {} 
RealMessage = []

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])


# Retrieve the message from your queue:
def get_message():
    for m in range(1, 11):
        try:
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
            
            # Check if there is a message in the queue or not
            if "Messages" in response:
                # extract the two message attributes you want to use as variables
                # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']
                # Print the message attributes - this is what you want to work with to reassemble the message
                # print(f"Order: {order}")
                # print(f"Word: {word}")

                # Storing message data in dictionary
                message = {order: word}
                AllMessages.update(message)

                # Delete each message 
                delete_message(handle)

            # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                # exit(1)
                continue

        # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])

# Trigger the function***
if __name__ == "__main__":
    get_message()

# Reassemble the phrase from the message content:
    # 1. sort your dictionary by key
    Sorted_Messages = dict(sorted(AllMessages.items()))

    # 2. fetch out the VALUES from the dict (another for loop)
    for val in Sorted_Messages.values():
        RealMessage.append(val)

# Testing / Debugging
    # print(AllMessages)
    # print(Sorted_Messages)

# Output the Message:
    print(RealMessage)