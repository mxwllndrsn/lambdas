## xlk button hit counter 

import boto3
import logging
from flask import Flask, request, jsonify
from botocore.exceptions import ClientError
from apig_wsgi import make_lambda_handler

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserCounters')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route('/xlk-user-counter-API', methods=['POST'])
def increment():
    username = request.json.get('username')
    try:
        response = table.update_item(
            Key = {'Username': username},
            UpdateExpression = 'ADD Counter :inc',
            ExpressionAttributeValues = {':inc': 1},
            ReturnValues = 'UPDATED_NEW'
        )
        return jsonify(response['Attributes']), 200
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500
    

@app.route('/xlk-user-counter-API', methods=['GET'])
def get_count():
    username = request.args.get('username')
    try: 
        response = table.get_item(Key = {'Username': username})
        if 'Item' in response:
            return jsonify(response['Item']), 200
        else: 
            return jsonify({'error': 'User not found'}), 404
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500 
    

lambda_handler = make_lambda_handler(app)

def lambda_logger(event, context):
    logger.info('event: '+ json.dumps(event))
    return lambda_handler(event, context)