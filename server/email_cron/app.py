import json
import traceback
from datetime import datetime
from connections import mongo_client
from sendgrid_intergration import send_email

mongo_obj = mongo_client()


def handler(event, context):
    try:
        curr_date = datetime.now().date().strftime("%d-%m-%Y")
        db = mongo_obj["future_note_emails"]
        collection = db[str(curr_date)]

        emails_to_send = list(collection.find({}))
        for emails in emails_to_send:
            content = emails["content"]
            email = emails["email"]
            print(content)
            print(email)
            resp = send_email(email, content)
            if resp["statusCode"] == 200:
                print(f"email sent to the email : {email}")
            else:
                print("Error in seding the email")
                # have a notification in place a webhook

        body = {
            "message": "function executed successfully!",
        }

        response = {"statusCode": 200, "body": json.dumps(body)}

        return response
    except Exception:
        print(f"Error in the handler function :{traceback.format_exc()}")


if __name__ == "__main__":
    handler(None, None)
