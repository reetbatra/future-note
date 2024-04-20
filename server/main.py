import threading
from time import sleep
from uuid import uuid4
from flask import Flask, request
from bson import json_util, ObjectId
from mongo_obj import get_mongo_client
from datetime import datetime, timedelta


app = Flask("future note")
thread_event = threading.Event()

KEYS_IN_USE = list()


@app.route('/', methods=['GET'])
def main():
    return "future note"


@app.route('/keys', methods=['POST'])
def generate_new_keys():
    request_data = request.get_json()

    new_key_resp = str(uuid4())
    response = {}

    # get no of keys to from user
    keys_list = list()
    if "no_of_keys" in request_data:
        response = {
            "key": str(new_key_resp),
            "available": True,
            "insert_time": datetime.now(),
        }
        if "email" in request_data:
            response["email"] = request_data["email"]
        keys_list.append(response)

    mongo_client = get_mongo_client()

    db = mongo_client["edra_labs"]
    collection = db["keys"]
    insert_ref = collection.insert_many(keys_list, ordered=True)
    print(insert_ref)

    mongo_client.close()
    return {
        "body": "keys generated"
    }


@app.route('/keys', methods=['GET'])
def get_keys():
    mongo_client = get_mongo_client()
    db = mongo_client["edra_labs"]
    collection = db["keys"]

    # res = collection.find({})
    # found_available_key = False

    # for key in res:
    #     if key["available"] is True:
    #         _id = key["_id"]
    #         res = collection.find_one_and_update({"_id": _id}, {
    #             "$set": {
    #                     "use_time": datetime.now(),
    #                     "available": False,
    #                     "last_use": datetime.now(),
    #                 },
    #             }
    #         )
    #         found_available_key = True
    #         break

    # TODO : add an index on available
    res = collection.find_one_and_update({"available": True}, {
        "$set": {
                "use_time": datetime.now(),
                "available": False,
                "last_use": datetime.now(),
            },
        }
    )
    if res is None:
        return {
            "statusCode": 404,
            "body": "no key found"
        }

    print(res)
    mongo_client.close()

    global KEYS_IN_USE
    KEYS_IN_USE.append(str(res["_id"]))
    # asyncio.run(key_in_use())
    thread_event.set()
    thread = threading.Thread(target=_is_key_in_use)
    thread.start()
    return {str(res["_id"]): res["key"]}


@app.route('/keys/', methods=['HEAD'])
def get_keys_metadata():
    _id = request.headers.get('id')

    mongo_client = get_mongo_client()
    db = mongo_client["edra_labs"]
    collection = db["keys"]

    res = collection.find_one({"_id": ObjectId(_id)})
    print(res)
    mongo_client.close()
    return json_util.dumps({
        "insert_time": res["insert_time"],
        "email": res["email"],
    })


@app.route('/keys/', methods=['DELETE'])
def delete_keys():
    _id = request.args.get('id')

    mongo_client = get_mongo_client()
    db = mongo_client["edra_labs"]
    collection = db["keys"]
    res = collection.delete_one({"_id": ObjectId(_id)})
    print(res)
    mongo_client.close()
    return {
        "body": "deleted"
    }


@app.route('/keys/', methods=['PUT'])
def unblock_keys():
    _id = request.headers.get('id')

    mongo_client = get_mongo_client()
    db = mongo_client["edra_labs"]
    collection = db["keys"]
    res = collection.find_one_and_update({"_id": ObjectId(_id)}, {
        "$set": {
                "free_time": datetime.now(),
                "available": True,
                "last_use": datetime.now()
            }
        }
    )

    print(res)

    global KEYS_IN_USE
    KEYS_IN_USE.remove(str(res["_id"]))
    return {
        "statusCode": 200,
        "body": "key freeed"
    }


@app.route('/keepalive', methods=['PUT'])
def keep_alive():
    _id = request.headers.get('id')

    mongo_client = get_mongo_client()
    db = mongo_client["edra_labs"]
    collection = db["keys"]

    res = collection.find_one_and_update({"_id": ObjectId(_id)}, {
        "$set": {
            "free_time": datetime.now(),
            "available": True,
            "last_use": datetime.now(),
            }
        }
    )
    print(res)

    return {
        "body": "requested key is alive for next 5 mins"
    }


@scheduler.task('interval', id='my_job', seconds=500)
def auto_delete_keys():
    mongo_client = get_mongo_client()
    db = mongo_client["edra_labs"]
    collection = db["keys"]
    res = collection.delete_many({
            "last_use": {"$lte": datetime.now()-timedelta(0, 300)}
        })
    print(f"deted keys: {res}")


if __name__ == '__main__':
    # auto_delete_keys()
    # scheduler.init_app(app)
    # scheduler.start()
    app.run(host='127.0.0.1', port=5000)
