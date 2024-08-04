import boto3
import json

def query_knowledge_base(question):
    client = boto3.client("bedrock-agent-runtime", region_name="eu-central-1")
    try:
        response = client.retrieve(
            knowledgeBaseId='WOVMY628MK',
            retrievalQuery={
                'text': question
            }            
        )
        answer = response['retrievalResults']
        text = list(map(lambda z: z['content']['text'], answer))
        return ', '.join(text)
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def answer(kb, items, question, history):
    runtime = boto3.client("bedrock-runtime", region_name="eu-central-1")
    messages = []
    if history:
        for h in history:
            messages.append(
                {
                    "role": h[0],
                    "content": [
                        {"type": "text", "text": h[1]},
                    ],
                })
    messages.append(
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
            ],
        }
    )
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.6,
            "system": f'You are a dental assistent that explains dental invoices to patients and knows the following information: {kb}. A patient has an invoice with the following items: {items}. Please answer the question of the patient. The patient speaks Dutch. You are only allowed to talk about the invoice items and the knowledge base information. If the patient ask something else just say that you are not allowed to talk about other topics.',
            "messages": messages,
        }
    )
    print(body)
    response = runtime.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=body
    )

    response_body = json.loads(response.get("body").read())
    return response_body['content'][0]['text']
    
def check_invoice(encoded_image):
    runtime = boto3.client("bedrock-runtime", region_name="eu-central-1")
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2,
            "temperature": 0.0,
            "system": 'You are provided to check documents. The user gonna provide you a document. Check if this document is a invoice. You are only allowed to return 1 word: "YES" or "NO" as a response.',
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
                        {"type": "text", "text": "Check this invoice."},
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
    answer = response_body['content'][0]['text']
    if answer == "YES":
        return True
    return False
    
def get_invoice_items(encoded_image):
    runtime = boto3.client("bedrock-runtime", region_name="eu-central-1")
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "temperature": 0.0,
            "system": 'You are a text extractor tool that reads items on invoices. The user gonna ask you to give a comma seperated list of the items on the included invoice. Perform this task in exactly this format: "ITEM 1, ITEM2, ITEM3". If you can not perform this task, please only return the text "FAILED".',
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
                        {"type": "text", "text": "On the given invoice, please give me a comma seperated list of the items."},
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
    if(response_body['content'][0]['text'] == "ERROR"):
        return "NO"
    m = response_body['content'][0]['text'].split(", ")
    return m


def handler(event, *args):
    body = json.loads(event['body'])
    if "image" in body:
        try:
            img = body['image']
            is_invoice = check_invoice(img)
            if not is_invoice:
                return {"status_code": 400, "error": "NOT_AN_INVOICE"}
            items = get_invoice_items(img)
            return {"status_code": 200, "items": items}
        except Exception as e:
            print(e)
            return {"status_code": 500, "error": "UNKNOWN"}
    if "question" in body and "items" in body:
        try:
            question = body['question']
            items = body['items']
            history = body.get('history', None)
            kb = query_knowledge_base(question)
            response = answer(kb, items, question, history)
            return {"status_code": 200, "answer": response}
        except Exception as e:
            print(e)
            return {"status_code": 500, "error": "UNKNOWN"}
    return {"status_code": 200}