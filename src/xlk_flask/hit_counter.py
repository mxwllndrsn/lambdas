## xlk button hit counter 

import boto3
import awsgi
from flask import Flask, request, jsonify
from botocore.exceptions import ClientError

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserCounters')


@app.route('/', methods=['POST'])
def index():
    ## increment count
    if request.method == 'POST':
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
    ## get count
    elif request.method == 'GET':
        username = request.args.get('username')
        try: 
            response = table.get_item(Key = {'Username': username})
            if 'Item' in response:
                return jsonify(response['Item']), 200
            else: 
                return jsonify({'error': 'User not found'}), 404
        except ClientError as e:
            return jsonify({'error': e.response['Error']['Message']}), 500 


def lambda_handler(event, context):
    return awsgi.response(app, event, context)