import json

class Invoice:
    def __init__(self, items):
        self.items = items

    def add_item(self, description, price):
        self.items.append({"description": description, "price": price})

    def get_string(self):
        str = ""
        for item in self.items:
            if 'description' in item:
                s = f"{item['description']}"
                if 'price' in item:
                    s += f" ({item['price']})"
                str += s + ", "
        return str
    
    def get_json_dump_items(self):
        return json.dumps(self.items)