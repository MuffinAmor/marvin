import json
import os

from lib.create import create_server, create_user

os.chdir(r'/home/niko/data/Marvin')


def edit_user_stats(server_id: str, user_id: str, stat: str, datas):
    create_user(server_id, user_id)
    if os.path.isfile("Server/{}/user.json".format(server_id)):
        with open("Server/{}/user.json".format(server_id), 'r') as fp:
            data = json.load(fp)
        data[user_id][stat] = datas
        with open("Server/{}/user.json".format(server_id, user_id), 'w') as fp:
            json.dump(data, fp, indent=4)


def set_message(server_id: str, name: str, message_id: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if name in data:
        data[name]['message'] = message_id
        with open('Server/{}/ticket.json'.format(server_id), "w+") as fp:
            json.dump(data, fp, indent=4)
    else:
        return False


def set_log(server_id: str, name: str, channel_id: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if name in data:
        data[name]['log'] = channel_id
        with open('Server/{}/ticket.json'.format(server_id), "w+") as fp:
            json.dump(data, fp, indent=4)
    else:
        return False


def set_category(server_id: str, name: str, category_id: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if name in data:
        data[name]['category'] = category_id
        with open('Server/{}/ticket.json'.format(server_id), "w+") as fp:
            json.dump(data, fp, indent=4)
    else:
        return False


def set_count(server_id: str, name: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if name in data:
        count = data[name]['ticket']
        data[name]['ticket'] = count + 1
        with open('Server/{}/ticket.json'.format(server_id), "w+") as fp:
            json.dump(data, fp, indent=4)
    else:
        return False


def edit_setting(server_id: str, vari: str, new):
    create_server(server_id)
    with open('Server/{}/settings.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if vari in data:
        data[vari] = new
        with open('Server/{}/settings.json'.format(server_id), "w+") as fp:
            json.dump(data, fp, indent=4)
    else:
        return False
