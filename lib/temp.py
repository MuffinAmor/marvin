import json
import os
from time import time


def set_join_time(server_id: str, user_id: str):
    if os.path.isfile("Server/{}/User/{}.json".format(server_id, user_id)):
        if os.path.isfile("Server/{}/Temp/time.json".format(server_id)):
            with open("Server/{}/Temp/time.json".format(server_id), "r") as fp:
                data = json.load(fp)
            data[user_id] = time()
            with open("Server/{}/Temp/time.json".format(server_id), "w") as fp:
                json.dump(data, fp, indent=4)


def request_join_time(server_id: str, user_id: str):
    if os.path.isfile("Server/{}/User/{}.json".format(server_id, user_id)):
        if os.path.isfile("Server/{}/Temp/time.json".format(server_id)):
            with open("Server/{}/Temp/time.json".format(server_id), "r") as fp:
                data = json.load(fp)
            return data[user_id]


def delete_temp_user(server_id: str, user_id: str):
    if os.path.isfile("Server/{}/User/{}.json".format(server_id, user_id)):
        if os.path.isfile("Server/{}/Temp/time.json".format(server_id)):
            with open("Server/{}/Temp/time.json".format(server_id), "r") as fp:
                data = json.load(fp)
            del data[user_id]
            with open("Server/{}/Temp/time.json".format(server_id), "w") as fp:
                json.dump(data, fp, indent=4)