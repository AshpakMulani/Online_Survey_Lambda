### CustomerSurvey-StackResourceDeployment(Lambda,DynamoDB).json : 

Stack JSON template creates below resources.
  >Used custom resource concept backed by inline lambda code for S3 upload from GitHub.
  
  >Custom resource can also used to create lex bot and add required utterances by survey. (not implemented in this version)
- Create S3 bucket to store lambda function source code.
-	Download lambda function source code from GitHub, Create .zip file and upload .zip to S3 bucket.
-	Create Role for lambda functions to provide full read-write access on Survey data DynamoDB table.
-	Create lambda execution role for CloudWatch log access.
-	Create three lambda functions referenced in Amazon connect call flows (GetSurveyData, GetOldSurveyResponse, FacilitiesSurvey)
-	Create DynamoDB table to store customer survey response with partition key as contact number.





### Lambda Function Code : 

##### FacilitiesSurvey.py   
      DOCSTRING:  This function is responsible for inserting caller's contact number and feedback for all survey
                  questions in Dynamo DB. FacilitiesSurvey-Question5 contact flow triggers this function at the end
                  of process after collecting caller's input for all survey questions.
      input:      default lambda_handler input.
                  event Dict gets ContactData Attributes from contact flow. Using generic names for customerfeedback<n>
                  variables to avoid renaming in case same survey gets used for some other purpose.
                  customerfeedback1 = CanteenFeedback, customerfeedback2 = CleaningFeedback , customerfeedback3 = GardeningFeedback,
                  customerfeedback4 = SecurityFeedback , customerfeedback5 = TransportFeedback
      output:     return Dict lambda_return = {"lambda_return":"0"} on success or lambda_return = {"lambda_return":"1"} on error.


#### GetOldSurveyResponse.py
      DOCSTRING:  This function is responsible for retrieving callers last recorded feedback using contact number from Dynamo DB.
      input:      Default lambda_handler input.
                  event Dict gets contact number using ContactData Attributes from contact flow.
      output:     return Dict "lambda_return" which contains  CustomerNumber, CanteenFeedback, CleaningFeedback, GardeningFeedback,
                  SecurityFeedback and TransportFeedback.
                  
#### GetSurveyData.py
      DOCSTRING:  This function is responsible for checking current caller has already completed survey by checking
                  caller's phone number in DynamoDB.
      input:      default lambda_handler input.
                  event Dict gets contact number using ContactData Attributes from contact flow.
      output:     return Dict lambda_return = {"exists":"0"} for first time caller or lambda_return = {"exists":"1"}
                  for return caller.
