#!/home/gitpod/.pyenv/shims/python3

# You have been given your own SQS queue, and some AWS credentials to use. 
# Write a single python script that does the following:
    # 1. Retrieves the messages that have been published to your queue. There are 10 in total.
    # 2. Each message contains two custom MessageAttributes: order and word. For instance, one message might contain an order of 3 and a word of what.
    # 3. You should determine some method for storing these values as a pair. There are many options: in a Python collection object, in a text file, an SQL database, a MongoDB collection, etc.
    # 4. Once you have picked up your messages, your python should reassemble the words by using the order value. This will reveal a phrase that you should then copy and paste into the phrase.txt file. DO NOT reassemble the messages by hand.
    # 5. Finally, your python should delete all messages after processing. This should not be done by hand.

import boto3
from botocore.exceptions import ClientError
import requests
import json
import collections
from collections import OrderedDict

# (1) Getting the message from your queue:

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/ktq3td"
sqs = boto3.client('sqs', region_name='us-east-1')

AllMessages = {} 
# Sorted_Messages = collections.OrderedDict(sorted(AllMessages.items()))

# Creates a sorted dictionary (sorted by key)
Sorted_Messages = OrderedDict(sorted(AllMessages.items()))
print(Sorted_Messages)

# sorted_dict = dict(sorted(AllMessages.items()))
# print(sorted_dict)


# def delete_message(handle):
#     try:
#         # Delete message from SQS queue
#         sqs.delete_message(
#             QueueUrl=url,
#             ReceiptHandle=handle
#         )
#         print("Message deleted")
#     except ClientError as e:
#         print(e.response['Error']['Message'])

def get_message():
    for m in range(1, 11):
        try:
        # We are trying to get message from SQS queue; each has two attributes (order and word)
        # Goal: extract those two attributes --> reassemble the message***
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

                message = {order: word}
                AllMessages.update(message)
    
                # delete here
                # delete_message(handle)


            # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                # exit(1)
                continue
            
        # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])

    # print(AllMessages)

    # TO DO
    # 1. sort your dictionary by key

    # 2. fetch out the VALUES from the dict (another for loop)

# Trigger the function***
if __name__ == "__main__":
    get_message()


# Determine your Queue URL: add UVA computing ID to the end of URL