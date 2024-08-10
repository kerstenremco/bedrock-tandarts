import boto3
import json
from models import Invoice

def create_session():
    import uuid
    id = str(uuid.uuid4())
    client = boto3.resource('dynamodb')
    table = client.Table('bedrock-dentibot')
    table.put_item(Item={'uid': id, 'key': 'metadata'})
    return id

def save_invoice(uid, invoice, items):
    client = boto3.resource('dynamodb')
    table = client.Table('bedrock-dentibot')
    table.put_item(Item={'uid': uid, 'key': 'invoice', 'invoice': invoice, 'invoice_items': items, 'history': []})

def add_history(uid, text, assistant=False):
    client = boto3.resource('dynamodb')
    table = client.Table('bedrock-dentibot')
    role = 'assistant' if assistant else 'user'
    result = table.update_item(
        Key={'uid': uid, 'key': 'invoice'},
        UpdateExpression='SET history = list_append(history, :q)',
        ExpressionAttributeValues={':q': [{'role': role, 'text': text}]},
        ReturnValues='ALL_NEW'
    )
    return result['Attributes']['history']

def get_items(uid):
    client = boto3.resource('dynamodb')
    table = client.Table('bedrock-dentibot')
    response = table.get_item(Key={'uid': uid, 'key': 'invoice'}, ProjectionExpression='invoice_items')
    return Invoice(json.loads(response['Item']['invoice_items']))