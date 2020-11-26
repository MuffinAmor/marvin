import json
import os
from time import time

os.chdir(r'/home/niko/data/Marvin')


def create_server(server_id: str):
    if not os.path.isdir("Server"):
        try:
            os.mkdir("Server")
        except FileExistsError:
            pass

    if not os.path.isdir("Server/{}".format(server_id)):
        try:
            os.mkdir("Server/{}".format(server_id))
        except FileExistsError:
            pass

    if not os.path.isdir("Server/{}/Shop".format(server_id)):
        try:
            os.mkdir("Server/{}/Shop".format(server_id))
        except FileExistsError:
            pass

    if not os.path.isdir("Server/{}/Temp".format(server_id)):
        try:
            os.mkdir("Server/{}/Temp".format(server_id))
        except FileExistsError:
            pass

    if not os.path.isdir("Server/{}/Toplist".format(server_id)):
        try:
            os.mkdir("Server/{}/Toplist".format(server_id))
        except FileExistsError:
            pass

    if not os.path.isdir("Server/{}/Toplist/Voice".format(server_id)):
        try:
            os.mkdir("Server/{}/Toplist/Voice".format(server_id))
        except FileExistsError:
            pass

    if not os.path.isdir("Server/{}/Toplist/Message".format(server_id)):
        try:
            os.mkdir("Server/{}/Toplist/Message".format(server_id))
        except FileExistsError:
            pass

    if not os.path.isfile("Server/{}/Shop/items.json".format(server_id)):
        data = {}
        with open("Server/{}/Shop/items.json".format(server_id), 'w') as fp:
            json.dump(data, fp, indent=4)

    if not os.path.isfile("Server/{}/Shop/shop.json".format(server_id)):
        data = {}
        with open("Server/{}/Shop/shop.json".format(server_id), 'w') as fp:
            json.dump(data, fp, indent=4)

    if not os.path.isfile("Server/{}/Temp/time.json".format(server_id)):
        data = {}
        with open("Server/{}/Temp/time.json".format(server_id), 'w') as fp:
            json.dump(data, fp, indent=4)

    if not os.path.isfile("Server/{}/user.json".format(server_id)):
        data = {}
        with open("Server/{}/user.json".format(server_id), 'w') as fp:
            json.dump(data, fp, indent=4)

    if not os.path.isfile("Server/{}/ticket.json".format(server_id)):
        data = {}
        with open("Server/{}/ticket.json".format(server_id), 'w+') as fp:
            json.dump(data, fp, indent=4)

    if not os.path.isfile("Server/{}/settings.json".format(server_id)):
        data = {'coins_per_message': 0,
                'coins_per_voice': 0,
                'time_delay': 0}
        with open("Server/{}/settings.json".format(server_id), 'w+') as fp:
            json.dump(data, fp, indent=4)


def create_user(server_id: str, user_id: str):
    create_server(server_id)
    with open("Server/{}/user.json".format(server_id), 'r') as fp:
        data = json.load(fp)
    if user_id not in data:
        data[user_id] = {
            'money': 0,
            'voice_time': 0,
            'message_count': 0,
            'last_message_time': time()
        }
        with open("Server/{}/user.json".format(server_id), 'w') as fp:
            json.dump(data, fp, indent=4)


def create_ticket_group(server_id: str, name: str):
    create_server(server_id)
    with open("Server/{}/ticket.json".format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if name not in data:
        data[name] = {
            'category': 0,
            'message': 0,
            'channel': [],
            'ticket': 1,
            'log': 0
        }
        with open('Server/{}/ticket.json'.format(server_id), "w+") as fp:
            json.dump(data, fp, indent=4)
        return 'The Ticketgroup **{}** has been created sucessfully.'.format(name)
    else:
        return 'This Ticketgroup is allready there.'


def create_ticket(server_id: str, name: str, channel_id: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    data[name]['channel'].append(channel_id)
    with open('Server/{}/ticket.json'.format(server_id), "w+") as fp:
        json.dump(data, fp, indent=4)
