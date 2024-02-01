## xlk button hit counter 

import boto3
import awsgi
import json
import logging
from flask import Flask, request, jsonify
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('xlk-user-counter')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route('/xlk-user-button-counter-increment', methods=['POST'])
def increment():
    username = request.json.get('username')

    if not username: 
        return jsonify({'error': 'username parameter is required'}), 400  

    try:
        response = table.update_item(
            Key = {'username': username},
            UpdateExpression = 'ADD pressCount :inc',
            ExpressionAttributeValues = {':inc': 1},
            ReturnValues = 'UPDATED_NEW'
        )
        return jsonify(response['Attributes']), 200
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500
    

@app.route('/xlk-user-button-counter-increment', methods=['GET'])
def get_count():
    username = request.args.get('username')

    if not username: 
        return jsonify({'error': 'username parameter is required'}), 400  

    try: 
        response = table.get_item(Key = {'username': username})
        if 'Item' in response:
            return jsonify(response['Item']), 200
        else: 
            return jsonify({'error': 'User not found'}), 404
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500 
    
    
@app.route('/xlk-user-button-counter-increment/total', methods=['GET'])
def get_total():
    try: 
        response = table.item_count
        return jsonify(response), 200
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500 


@app.errorhandler(404)
def invalid_route(e):
    return "404 error - route not found"

def lambda_handler(event, context):
    logger.info(json.dumps(event))
    return awsgi.response(app, event, context)