import json
import os

import sys

os.chdir(r'/home/niko/data/Marvin')


def refactor_shop(server_id: str):
    try:
        data = {}
        with open("Server/{}/Shop/shop.json".format(server_id), 'w+') as fp:
            json.dump(data, fp, indent=4)
        with open("Server/{}/Shop/items.json".format(server_id), encoding="utf-8") as fp:
            datas = json.load(fp)
        s = 0
        liste = []
        max = round(len(datas) / 5)
        for n in range(max + 1):
            data[n] = {}
            for s, i in enumerate(datas):
                if i not in liste:
                    if s % 5 == 0:
                        break
                    data[n][i] = {}
                    liste.append(n)

        with open("Server/{}/Shop/shop.json".format(server_id), 'w+') as fp:
            json.dump(data, fp, indent=4)
        for n, i in enumerate(list(datas)):
            if (n + 1) % 5 == 0:
                s = s + 1
            token = str(i)
            name = datas[token]['Rollename']
            Preis = datas[token]['Preis']
            data[s][i] = {'role_name': name,
                          'price': Preis,
                          }
            with open("Server/{}/Shop/shop.json".format(server_id), 'w+') as fp:
                json.dump(data, fp, indent=4)
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def add_market_item(server_id: str, role_name: str, role_id: str, role_price: int):
    try:
        with open("Server/{}/Shop/items.json".format(server_id), encoding="utf-8") as fp:
            data = json.load(fp)
        if role_id in data:
            return "The Role is already in the Shop."
        data[role_id] = {'Rollename': role_name,
                         'RollenID': role_id,
                         'Preis': role_price}
        with open("Server/{}/Shop/items.json".format(server_id), 'w+') as fp:
            json.dump(data, fp, indent=4)
        refactor_shop(server_id)
        return "The Role **{}** has been added sucessfully to the Role Shop".format(role_name)

    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def remove_market_item(server_id: str, item: str):
    try:
        with open("Server/{}/Shop/items.json".format(server_id), encoding="utf-8") as fp:
            data = json.load(fp)
            if str(item) in str(data):
                name = data[item]['Rollename']
                del data[item]
                with open("Server/{}/Shop/items.json".format(server_id), 'w+') as fp:
                    json.dump(data, fp, indent=4)
                refactor_shop(server_id)
                return 'The Role **{}** has been removed sucessfully from the Shop.'.format(name)
            else:
                return "I don't have found a Role with that Key. Please try again."
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def create_market_UI(server_id: str, seite: int):
    try:
        if seite > extreme_market(server_id, 'max') or seite < 0:
            return None
        else:
            refactor_shop(server_id)
        with open("Server/{}/Shop/shop.json".format(server_id), encoding="utf-8") as fp:
            data = json.load(fp)
        UI = ""
        sites = len(data)
        site = str(seite)
        for i in data[site]:
            UI += "Role: {}\n" \
                  "Coins: {}\n\n".format(data[site][i]['role_name'], data[site][i]['price'])
        if UI == "":
            UI += "This Place is empty."
        else:
            UI += "Site {} of {}\n\n".format(int(site) + 1, sites)
        return UI
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


# def get_token(n: int):
#    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def checkif(server_id: str, item: str):
    with open("Server/{}/Shop/items.json".format(server_id), encoding="utf-8") as fp:
        data = json.load(fp)
    if item in list(data):
        return True
    else:
        return False


def get_info(server_id: str, item: str, stat: str):
    with open("Server/{}/Shop/items.json".format(server_id), encoding="utf-8") as fp:
        data = json.load(fp)
    if item in list(data):
        return data[item][stat]


def extreme_market(server_id: str, para: str):
    with open("Server/{}/Shop/items.json".format(server_id), encoding="utf-8") as fp:
        data = json.load(fp)
    if para == "max":
        return len(data)
