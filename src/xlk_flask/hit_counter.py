## xlk button hit counter 

import boto3
import awsgi
import json
import logging
from flask import Flask, request, jsonify
from botocore.exceptions import ClientError

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('xlk_user_button_hit_counter')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

@app.route('/xlk-user-button-counter-increment', methods=['POST', 'GET'])
def index():
    ## increment count
    if request.method == 'POST':
        username = request.json.get('username')

        if not username: 
            return jsonify({'error': 'Username parameter is required'}), 400  
        
        try:
            response = table.update_item(
                Key = {'Username': username},
                UpdateExpression = 'ADD total_hit :inc',
                ExpressionAttributeValues = {':inc': 1},
                ReturnValues = 'UPDATED_NEW'
            )
            return jsonify(response['Attributes']), 200
        except ClientError as e:
            return jsonify({'error': e.response['Error']['Message']}), 500
        
    ## get count
    elif request.method == 'GET':
        username = request.args.get('username')    

        if not username:  
            return jsonify({'error': 'Username parameter is required'}), 400
        
        try: 
            response = table.get_item(Key = {'Username': username})
            if 'Item' in response:
                return jsonify(response['Item']), 200
            else: 
                return jsonify({'error': 'User not found'}), 404
        except ClientError as e:
            return jsonify({'error': e.response['Error']['Message']}), 500 

@app.errorhandler(404)
def invalid_route(e):
    return "oh god oh fuck"

def lambda_handler(event, context):
    logger.info(json.dumps(event))
    return awsgi.response(app, event, context)