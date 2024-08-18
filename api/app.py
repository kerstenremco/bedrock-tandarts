import json
import anthropic
import knowledge_base
import session

def generate_response(status_code=200, error=None, body=None, uid=None):
    response = {
        "statusCode": status_code,
    }
    if uid:
        response["uid"] = uid
    if error:
        response["error"] = error
    if body:
        response["body"] = body
    return json.dumps(response)

def handle_image(img):
    try:
        s = session.Session()
        # Check if is invoice
        try:
            is_invoice = s.setImage(img)
            if not is_invoice:
                return generate_response(status_code=400, uid=s.uid, error="NOT_AN_INVOICE")
        except Exception as e:
            print("Error setting image: ", e)
            return generate_response(status_code=500, uid=s.uid, error="UNKNOWN")
        # Get items
        try:
            s.load_invoice()
        except Exception as e:
            print("Error getting items: ", e)
            generate_response(status_code=500, uid=s.uid, error="UNKNOWN")
        # Check if dental
        try:
            valid = s.check_dental()
            if not valid:
                return generate_response(status_code=400, uid=s.uid, error="NOT_AN_DENTAL_INVOICE")
        except Exception as e:
            print("Error checking dental: ", e)
            return generate_response(status_code=500, uid=s.uid, error="UNKNOWN")
        # Return uid and items
        return generate_response(uid=s.uid, body=s.invoice.items)
    except Exception as e:
        print(e)
        return generate_response(status_code=500, error="UNKNOWN")
    
def handle_confirmation(uid, confirmed):
    try:
        s = session.Session.load(uid)
        s.confirm(confirmed)
        if confirmed:
            return generate_response(uid=s.uid, body=s.invoice.items)
        else:
            return generate_response()
    except Exception as e:
        print(e)
        return generate_response(status_code=500, error="UNKNOWN")
    
def handle_question(uid, question):
    try:
        s = session.Session.load(uid)
        s.add_history(question=question)
        kb = knowledge_base.query_knowledge_base(question)
        answer = anthropic.answer(kb, s.invoice.get_json_dump(), s.history)
        s.add_history(answer=answer)
        return generate_response(uid=s.uid, body=answer)
    except Exception as e:
        print(e)
        return {"status_code": 500, "error": "UNKNOWN"}

def handler(event, *args):
    body = json.loads(event['body'])
    if "image" in body:
        response = handle_image(body['image'])
        return response
    if "confirmed" in body and "uid" in body:
        response = handle_confirmation(body['uid'], body['confirmed'])
        return response
    if "question" in body and "uid" in body:
        response = handle_question(body['uid'], body['question'])
        return response
    return generate_response(status_code=400, error="UNKNOWN_REQUEST")