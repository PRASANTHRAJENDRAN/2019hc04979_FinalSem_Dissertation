import os
import io
import boto3
import json
import csv

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker',aws_access_key_id = '<aws_access_key_id>',aws_secret_access_key = '<aws_secret_access_key>',region_name = 'ap-southeast-1')

def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    
    requestBody = json.loads(json.dumps(event))
    print('requestBody: {}'.format(requestBody))
    usedStorage = str(requestBody['usedStorage'])
    userInvites = str(requestBody['userInvites'])
    usersCount = str(requestBody['usersCount'])
    activitiesCount = str(requestBody['activitiesCount'])
    payload = ",".join([usedStorage, userInvites, usersCount, activitiesCount])
    print('payload: {}'.format(payload))
    inference_response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='text/csv',
                                        Accept = 'text/csv',
                                       Body=payload)

    result = json.loads(inference_response['Body'].read().decode())
    print('result {}'.format(result))
    response = float(result) * 100
    if  response > 90: 
        result = "Yes"
        possibility = "High"
        message = "Input user is a potential candidate for Premium upgrade"
    else:
        result = "No"
        possibility = "Low"
        message = "Input user is not a potential candidate for Premium upgrade"
    responseBody = {
        "result": result,
        "possibility": possibility,
        "message": message
    }  
    print('reponse body: {}'.format(responseBody))
    return responseBody
