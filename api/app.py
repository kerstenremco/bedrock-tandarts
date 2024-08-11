import json
import db
import anthropic
import knowledge_base

def handle_image(img):
    try:
        uid = db.create_session()
        is_invoice = anthropic.check_invoice(img)
        if not is_invoice:
            return {"status_code": 400, "error": "NOT_AN_INVOICE"}
        items = anthropic.get_invoice_items(img)
        valid = anthropic.check_invoice_dental(items.get_string())
        if not valid:
            return {"status_code": 400, "error": "NOT_A_DENTAL_INVOICE"}
        db.save_invoice(uid, img, items.get_json_dump_items())
        return {"status_code": 200, "uid": uid, "items": items.get_string()}
    except Exception as e:
        print(e)
        return {"status_code": 500, "error": "UNKNOWN"}
    
def handle_question(uid, question):
    try:
        items = db.get_items(uid)
        history = db.add_history(uid, question)
        kb = knowledge_base.query_knowledge_base(question)
        response = anthropic.answer(kb, items.get_string(price=True), history)
        db.add_history(uid, response, assistant=True)
        return {"status_code": 200, "answer": response}
    except Exception as e:
        print(e)
        return {"status_code": 500, "error": "UNKNOWN"}

def handler(event, *args):
    body = json.loads(event['body'])
    if "image" in body:
        response = handle_image(body['image'])
        return response
    if "question" in body and "uid" in body:
        response = handle_question(body['uid'], body['question'])
        return response
    return {"status_code": 400}