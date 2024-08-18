import boto3

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
        return f"An error occurred in query KB: {str(e)}"