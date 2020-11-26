import json
import os

from lib.create import create_server

os.chdir(r'/home/niko/data/Marvin')


def delete_server(server_id: str):
    if os.path.isfile("Server/{}".format(server_id)):
        os.remove("Server/{}".format(server_id))


def delete_user(server_id: str, user_id: str):
    create_server(server_id)
    with open("Server/{}/user.json".format(server_id), 'r') as fp:
        data = json.load(fp)
    if user_id in data:
        del data[user_id]
        with open("Server/{}/user.json".format(server_id), 'w') as fp:
            json.dump(data, fp, indent=4)


def delete_ticket(server_id: str, name: str, channel_id: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    data[name]['channel'].remove(channel_id)
    with open('Server/{}/ticket.json'.format(server_id), "w+") as fp:
        json.dump(data, fp, indent=4)


def delete_group(server_id: str, name: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if name in data:
        del data[name]
        with open('Server/{}/ticket.json'.format(server_id), "w+") as fp:
            json.dump(data, fp, indent=4)
        return "The Ticket-Group {} has been deleted".format(name)
    else:
        return "The Ticket-Group {} is not found.".format(name)
