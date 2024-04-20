import traceback


def handler(event, context):
    try:
        print("handler invoked")
        body = event["body"]

    except Exception:
        print(f"Error in the handler execution : {traceback.format_exc()}")
