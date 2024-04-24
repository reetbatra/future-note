import traceback
from datetime import datetime
from connections import mongo_client

mongo_obj = mongo_client()


def handler(event, context):
    try:
        print(f"handler invoked, event: {event}")
        if "email" in event:
            print("have the email to send the mail to")
            # mongo insert
            date_to_send = event["date_to_send"]
            db = mongo_obj["future_note_emails"]
            collection = db[date_to_send]
            _insert_obj = {
                "date": date_to_send,
                "email": event["email"],
                "content": event["content"],
                "insert_time": datetime.now(),
            }
            collection.insert_one(_insert_obj)
            return {
                "body": "inserted successfully",
                "statusCode": 200,
            }
        else:
            return {
                "body": "email is not present in the body",
                "statusCode": 404,
            }
    except Exception:
        print(f"Error in the handler execution : {traceback.format_exc()}")
