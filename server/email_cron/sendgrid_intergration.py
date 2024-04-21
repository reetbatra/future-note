import os
import sendgrid
import traceback
from sendgrid.helpers.mail import Mail, Email, To, Content


def send_email(email_to_send, email_content):
    try:
        print("inside the send email funciton")
        sg = sendgrid.SendGridAPIClient(
            api_key=os.environ.get('SENDGRID_API_KEY')
        )
        from_email = Email("test@example.com")  # TODO: change the eamil
        to_email = To(email_to_send)
        subject = "A message to you from the Future Note"
        content = Content(email_content)
        mail = Mail(from_email, to_email, subject, content)

        mail_json = mail.get()

        response = sg.client.mail.send.post(request_body=mail_json)
        print(response.status_code)
        print(response.headers)
        resp = {
            "statusCode": 200,
            "message": "success",
        }
        return resp
    except Exception:
        print(
            f"error in sending the email: {traceback.format_exc()}"
        )
        erro_mssg = traceback.format_exc()
        resp = {
            "statusCode": 500,
            "message": "error " + erro_mssg,
        }
        return resp
