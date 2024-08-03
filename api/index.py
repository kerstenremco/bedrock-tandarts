import boto3
import json

def query_knowledge_base(query):
    client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    try:
        response = client.retrieve_and_generate(
            input={
                'text': query
            },
            retrieveAndGenerateConfiguration={
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': 'EQSVCSFERG',
                    'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
                },
                'type': 'KNOWLEDGE_BASE'
            },
            
        )
        return response['output']['text']
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def get_invoice_items(encoded_image):
    runtime = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": encoded_image,
                            },
                        },
                        {"type": "text", "text": "Which items are on this invoice? Give me only a comma seperated list with the items without further text. If this is not an invoice or you can't read it, just say ERROR"},
                    ],
                }
            ],
        }
    )

    response = runtime.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=body
    )

    response_body = json.loads(response.get("body").read())
    if(response_body['content'][0]['text'] == "ERROR"):
        return "NO"
    m = response_body['content'][0]['text'].split(", ")
    return m


def handler(event, context):
    body = json.loads(event['body'])
    if "image" in body:
        img = body['image']
        items = get_invoice_items(img)
        print(items)
        return json.dumps({'items': items})
    if "item" in body:
        item = body['item']
        query = f"Geef me een uitleg over mijn tandartsfactuur met de volgende regel: {item}. Houdt geen rekening met eventuele code's"
        results = query_knowledge_base(query)
        return json.dumps({'answer': results})
    
    
    
