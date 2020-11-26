import json
import os

from lib.create import create_server, create_user

os.chdir(r'/home/niko/data/Marvin')


def request_user_stats(server_id: str, user_id: str, stat: str):
    create_user(server_id, user_id)
    if os.path.isfile("Server/{}/user.json".format(server_id)):
        with open("Server/{}/user.json".format(server_id), 'r') as fp:
            data = json.load(fp)
        return data[user_id][stat]


def request_ticket(server_id: str, name: str):  # überarbeiten mit token zuweisen
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if name in data:
        return data[name]['ticket']
    else:
        return False


def request_channel(server_id: str, name: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if name in data:
        return data[name]['channel']
    else:
        return False


def request_log(server_id: str, name: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if name in data:
        return data[name]['log']
    else:
        return False


def request_name_message(server_id: str, message_id: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    for i in data:
        if data[i]['message'] == message_id:
            return i
    else:
        return False


def request_name_category(server_id: str, category_id: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    for i in data:
        if data[i]['category'] == category_id:
            return i
    else:
        return False


def request_name_channel(server_id: str, channel_id: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    for i in data:
        if channel_id in data[i]['channel']:
            return i
    else:
        return False


def request_category(server_id: str, name: str):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if name in data:
        return data[name]['category']
    else:
        return False


def request_groups(server_id: str, value: str, group: str = None):
    create_server(server_id)
    with open('Server/{}/ticket.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if value == "single":
        if str(group) in list(data):
            return True
    elif value == "liste":
        liste = []
        for i in data:
            liste.append(i)
            return "\n".join(liste)
        else:
            return "No Ticketgroups"


def request_setting(server_id: str, vari: str):
    create_server(server_id)
    with open('Server/{}/settings.json'.format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    if vari in data:
        return data[vari]
    else:
        return False
