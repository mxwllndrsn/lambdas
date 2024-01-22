# xlk button hit counter 

from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError


app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserCounters')


@app.route('/counter', methods=['POST'])
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
    

@app.route('/counter', methods=['GET'])
def get_count():
    username = request.args.get('username')
    try: 
        response = table.get_item(Key = {'Username': username})
        if 'Item' in response:
            return jsonify(resposne['Item']), 200
        else: 
            return jsonify({'error': 'User not found'}), 404
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500 
    

# aws wsgi lambda handler
from aws_wsgi import make_lambda_handler
lambda_handler = make_lambda_handler(app)

## testing