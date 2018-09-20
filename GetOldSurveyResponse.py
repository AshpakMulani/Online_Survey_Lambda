import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    '''
    DOCSTRING:  This function is responsible for retrieving callers last recorded feedback using contact number from Dynamo DB.

    input:      Default lambda_handler input.
                event Dict gets contact number using ContactData Attributes from contact flow.

    output:     return Dict "lambda_return" which contains  CustomerNumber, CanteenFeedback, CleaningFeedback, GardeningFeedback,
                SecurityFeedback and TransportFeedback.
    '''

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FacilitiesSurveyData')

    # retrieving contact number from contact flow attributes. 'contactnumber' is contact attribute holding
    # current caller's phone number.
    contactnumber = event['Details']['ContactData']['Attributes']['contactnumber']

    lambda_return = {}

    try:
        response = table.get_item(
            Key={
                'contactnumber': contactnumber
            }
        )
    except ClientError as e:
        # returning zero on error. It makes contact flow to treat current caller as first time caller.
        lambda_return['exists'] = 0
        return lambda_return
    else:
        # For no matching record in DynamoDB Response['Item'] will not have ['contactnumber']
        if response.get('Item', {}).get('contactnumber') is None:
            # returning zero if callers number does not exists in DB, It makes contact flow to treat current
            # caller as first time caller.
            lambda_return['exists'] = 0
        else:
            #return details from DynamoDB if callers contact number is matching with stored contact number
            #(returned caller)
            lambda_return = response['Item']
        return lambda_return