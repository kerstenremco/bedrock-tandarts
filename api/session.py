
import boto3
from datetime import datetime
import anthropic
from invoice import Invoice
db = boto3.resource('dynamodb')
import knowledge_base
import concurrent.futures

table = db.Table('bedrock-dentibot')

class Session:
    def __init__(self, empty=False):
        if empty:
            return
        import uuid
        self.uid = str(uuid.uuid4())
        self.ts = datetime.timestamp(datetime.now())
        self.history = []
        table.put_item(Item={'uid': self.uid, 'key': 'metadata', 'ts': str(self.ts), 'history': []})

    @classmethod
    def load(cls, uid):
        self = cls(empty=True)
        self.uid = uid
        response = table.get_item(Key={'uid': self.uid, 'key': 'metadata'})
        self.ts = response['Item']['ts']
        self.is_invoice = response['Item'].get('is_invoice')
        invoice_data = response['Item'].get('invoice')
        if invoice_data:
            self.invoice = Invoice(items=invoice_data)
        self.dental_invoice = response['Item'].get('dental_invoice')
        self.confirmed = response['Item'].get('confirmed')
        self.history = response['Item'].get('history')
        return self
    
    def setImage(self, img):
        self.image = img
        self.is_invoice = anthropic.check_invoice(self.image)
        table.update_item(
            Key={'uid': self.uid, 'key': 'metadata'},
            UpdateExpression='SET is_invoice = :ii',
            ExpressionAttributeValues={':ii': self.is_invoice}
        )
        return self.is_invoice
    
    def load_invoice(self):
        self.invoice = anthropic.get_invoice_items(self.image)
        table.update_item(
            Key={'uid': self.uid, 'key': 'metadata'},
            UpdateExpression='SET invoice = :invoice',
            ExpressionAttributeValues={':invoice': self.invoice.items}
        )
    def check_dental(self):
        self.dental_invoice = anthropic.check_invoice_dental(self.invoice.get_string())
        table.update_item(
            Key={'uid': self.uid, 'key': 'metadata'},
            UpdateExpression='SET dental_invoice = :di',
            ExpressionAttributeValues={':di': self.dental_invoice}
        )
        return self.dental_invoice
    
    def confirm(self, confirmed):
        if not confirmed:
            self.confirmed = False
            table.update_item(
                Key={'uid': self.uid, 'key': 'metadata'},
                UpdateExpression='SET confirmed = :confirmed',
                ExpressionAttributeValues={':confirmed': False}
            )
        else:
            self.confirmed = True
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.__process_item, item): item for item in self.invoice.items}
                for future in concurrent.futures.as_completed(futures):
                    item = futures[future]
                    response = future.result()
                    item['explanation'] = response
            table.update_item(
                Key={'uid': self.uid, 'key': 'metadata'},
                UpdateExpression='SET confirmed = :confirmed, invoice = :invoice',
                ExpressionAttributeValues={':confirmed': True, ':invoice': self.invoice.items}
            )

    def __process_item(self, item):
        text = f"Code: {item['code']}. Omschrijving: {item['description']}."
        kb = knowledge_base.query_knowledge_base(text)
        response = anthropic.get_explanation_for_item(kb, text)
        return response

    def add_history(self, question=None, answer=None):
        role = 'assistant' if answer else 'user'
        text = answer if answer else question
        item = {'role': role, 'text': text}
        self.history.append(item)
        table.update_item(
        Key={'uid': self.uid, 'key': 'metadata'},
        UpdateExpression='SET history = list_append(history, :q)',
        ExpressionAttributeValues={':q': [item]}
        )