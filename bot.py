import datetime
import time
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from twilio.rest import Client

with open("config.json") as f:
    data = json.load(f)
    AVALON_SAN_BRUNO_LINK = data["AVALON_SAN_BRUNO_LINK"]
    account_sid = data["account_sid"]
    auth_token = data["auth_token"]
    Sender = data["Sender"]
    Reciver = data["Reciver"]


def polling_avalon_price():
    content = urlopen(AVALON_SAN_BRUNO_LINK).read()
    soup = BeautifulSoup(content, 'html.parser')

    price_details = soup.findAll("div", {"class": "price"})
    room_details = soup.findAll("div", {"class": "details"})

    return [price.text + " " + room.text for price, room in zip(price_details, room_details)]


def send_msg(result):
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body="As for {}, {} units are available. \n"
                 "{}".format(date_time, len(result), " \n".join(result)),

            from_=Sender,

            to=Reciver

        )
        print("send msg at {}".format(datetime))
    except Exception as e:
        print(e)


def run():
    while True:
        res = polling_avalon_price()
        send_msg(res)
        time.sleep(14400)


if __name__ == '__main__':
    run()