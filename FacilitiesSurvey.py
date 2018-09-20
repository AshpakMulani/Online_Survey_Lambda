import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    '''
    DOCSTRING:  This function is responsible for inserting caller's contact number and feedback for all survey
                questions in Dynamo DB. FacilitiesSurvey-Question5 contact flow triggers this function at the end
                of process after collecting caller's input for all survey questions.

    input:       default lambda_handler input.
                event Dict gets ContactData Attributes from contact flow. We are keeping generic names for customerfeedback<n>
                variables to avoid renaming in case same survey gets used for some other purpose.
                customerfeedback1 = CanteenFeedback, customerfeedback2 = CleaningFeedback , customerfeedback3 = GardeningFeedback,
                customerfeedback4 = SecurityFeedback , customerfeedback5 = TransportFeedback

    output:     return Dict lambda_return = {"lambda_return":"0"} on success or lambda_return = {"lambda_return":"1"} on error.
    '''

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FacilitiesSurveyData')
    lambda_return = {}

    try:
        # retrieving contact number and customer feedback from contact flow attributes.
        contactnumber = event['Details']['ContactData']['Attributes']['contactnumber']
        customerfeedback1 = event['Details']['ContactData']['Attributes']['customerfeedback1']
        customerfeedback2 = event['Details']['ContactData']['Attributes']['customerfeedback2']
        customerfeedback3 = event['Details']['ContactData']['Attributes']['customerfeedback3']
        customerfeedback4 = event['Details']['ContactData']['Attributes']['customerfeedback4']
        customerfeedback5 = event['Details']['ContactData']['Attributes']['customerfeedback5']

        # Inserting values in Dynamo DB by preparing Item Dict from collected user feedback.
        response = table.put_item(
            Item={
                'CanteenFeedback': customerfeedback1,
                'CleaningFeedback': customerfeedback2,
                'GardeningFeedback': customerfeedback3,
                'SecurityFeedback': customerfeedback4,
                'TransportFeedback': customerfeedback5,
                'contactnumber': str(contactnumber)

            }
        )

    except ClientError as e:
        lambda_return['lambda_return'] = 1
        return lambda_return
    else:
        lambda_return['lambda_return'] = 0
        return lambda_return

