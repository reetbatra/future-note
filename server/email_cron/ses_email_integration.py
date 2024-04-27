import os
import boto3
import traceback
from botocore.exceptions import ClientError

AWS_ACCESS_ID = os.getenv("AWS_ACCESS_ID")
AWS_ACCESS_KEY_VAL = os.getenv("AWS_ACCESS_KEY_VAL")
AWS_REGION_VAL = os.getenv("AWS_REGION_VAL")


class SesDestination:
    def __init__(self, tos, ccs=None, bccs=None):
        self.tos = tos
        self.ccs = ccs
        self.bccs = bccs

    def to_service_format(self):
        svc_format = {"ToAddresses": self.tos}
        if self.ccs is not None:
            svc_format["CcAddresses"] = self.ccs
        if self.bccs is not None:
            svc_format["BccAddresses"] = self.bccs
        return svc_format


class SesMailSender:
    def __init__(self, ses_client):
        self.ses_client = ses_client

    def send_email(self, destination, html, text="", reply_tos=None):
        send_args = {
            "Source": "ruwaliharshit@gmail.com",
            "Destination": destination.to_service_format(),
            "Message": {
                "Subject": {"Data": "A note to youself form the past you!"},
                "Body": {"Text": {"Data": text}, "Html": {"Data": html}},
            },
        }
        if reply_tos is not None:
            send_args["ReplyToAddresses"] = reply_tos
        try:
            response = self.ses_client.send_email(**send_args)
            message_id = response["MessageId"]
            print("Sent mail %s from %s to %s.", message_id, destination)
        except ClientError:
            print("Couldn't send mail from %s to %s.", destination)
            erro_mssg = traceback.format_exc()
            resp = {
                "statusCode": 500,
                "message": "error " + erro_mssg,
            }
            return resp
        else:
            return {
                "statusCode": 200,
                "message": "success",
            }


def send_email(email, text):
    ses_client = boto3.client(
        "ses",
        region_name=AWS_REGION_VAL,
        aws_access_key_id=AWS_ACCESS_ID,
        aws_secret_access_key=AWS_ACCESS_KEY_VAL,
    )
    ses_mail_sender = SesMailSender(ses_client)
    return ses_mail_sender.send_email(SesDestination([email]), text)
