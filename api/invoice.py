import json

class Invoice:
    def __init__(self, items=[]):
        self.items = []
        c = 0
        for item in items:
            if 'description' in item:
                c += 1
                i = {'id': c}
                i['description'] = item['description']
                if 'price' in item:
                    i['price'] = str(item['price'])
                if 'amount' in item:
                    i['amount'] = item['amount']
                if 'code' in item:
                    i['code'] = item['code']
                self.items.append(i)

    # def add_item(self, description, price):
    #     self.items.append({"description": description, "price": price})

    def get_string(self):
        str = ""
        for item in self.items:
            if 'description' in item:
                s = ""
                if 'amount' in item:
                    s += f"{item['amount']} x "
                if 'code' in item:
                    s += f"Code {item['code']}. "
                s += f"Description: {item['description']}."
                if 'price' in item:
                    s += f" Price: {item['price']}"
                str += s + "\n"
        return str
    
    def get_json_dump(self):
        return json.dumps(self.items)

    @classmethod
    def from_json(cls, json_str):
        return cls(json.loads(json_str))