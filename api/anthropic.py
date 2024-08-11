import json
import boto3
from models import Invoice

def answer(kb, items, history):
    runtime = boto3.client("bedrock-runtime", region_name="eu-central-1")
    messages = []
    for h in history:
        messages.append(
            {
                "role": h['role'],
                "content": [
                    {"type": "text", "text": h['text']},
                ],
            })
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.6,
            "system": f'You are a dental assistent that explains dental invoices to patients and knows the following information: {kb}. A patient has an invoice with the following items: {items}. Please answer the question of the patient. The patient speaks Dutch. You are only allowed to talk about the invoice items and the knowledge base information. If the patient ask something else just say that you are not allowed to talk about other topics.',
            "messages": messages,
        }
    )
    response = runtime.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=body
    )

    response_body = json.loads(response.get("body").read())
    return response_body['content'][0]['text']

def check_invoice_dental(items):
    runtime = boto3.client("bedrock-runtime", region_name="eu-central-1")
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2,
            "temperature": 0.0,
            "system": 'You are provided to check if items on an invoice are from a dentist.',
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{items}. Are those invoice items from a dentist?. Answer with (YES) if it are invoice items from a dentist, otherwise answer with (NO)."},
                        
                    ],
                },
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": "("},
                        
                    ],
                }
            ],
        }
    )
    response = runtime.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=body
    )

    response_body = json.loads(response.get("body").read())
    answer = f"({response_body['content'][0]['text']}"
    if answer == "(YES)":
        return True
    if answer == "(NO)":
        return False
    raise Exception("Invalid response")
    
def check_invoice(encoded_image):
    runtime = boto3.client("bedrock-runtime", region_name="eu-central-1")
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2,
            "temperature": 0.0,
            "system": 'You are provided to check documents. The user gonna provide you a document. Check if this document is a invoice.',
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
                        {"type": "text", "text": "Check this invoice. Answer with (YES) if it is a invoice, otherwise answer with (NO)."},
                        
                    ],
                },
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": "("},
                        
                    ],
                }
            ],
        }
    )
    response = runtime.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=body
    )

    response_body = json.loads(response.get("body").read())
    answer = f"({response_body['content'][0]['text']}"
    if answer == "(YES)":
        return True
    if answer == "(NO)":
        return False
    raise Exception("Invalid response")


    
def get_invoice_items(encoded_image):
    runtime = boto3.client("bedrock-runtime", region_name="eu-central-1")
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "temperature": 0.0,
            "system": 'You are provided to check extract items from invoices. The user gonna provide you a document.',
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
                        {"type": "text", "text": "Get the items on this invoice. Return an array with a JSON object for items. Each JSON item in the array must contain the description, and a price if applicable. If you can't find any items return an empty array without items."},
                    ],
                },
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": "["},
                    ],
                }
            ],
        }
    )

    response = runtime.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=body
    )

    response_body = json.loads(response.get("body").read())
    answer = f"[{response_body['content'][0]['text']}"
    # Check if the response is an array
    if not answer.startswith("[") or not answer.endswith("]"):
        print(answer)
        raise Exception("Invalid response")
    list_items = json.loads(answer.replace("\n", "").strip())
    return Invoice(list_items)