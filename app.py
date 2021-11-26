import telepot
import pprint
import requests
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or None
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') or None
TABLETKIUA_SN = os.environ.get('TABLETKIUA_SN') or None
TABLETKIUA_API_USERNAME = os.environ.get('TABLETKIUA_API_USERNAME') or None
TABLETKIUA_API_PASSWORD = os.environ.get('TABLETKIUA_API_PASSWORD') or None
TABLETKI_URL = "https://reserve.tabletki.ua/api/orders"


def send_message(message_text):
    escaped_message = escapeSymbolsForTelegram(message_text)
    bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
    bot.sendMessage(TELEGRAM_CHAT_ID, escaped_message, parse_mode='MarkdownV2')


def escapeSymbolsForTelegram(raw_message):
    escaped_message = raw_message.replace("+", "\+")
    escaped_message = escaped_message.replace(".", "\.")
    escaped_message = escaped_message.replace("-", "\-")
    escaped_message = escaped_message.replace("(", "\(")
    escaped_message = escaped_message.replace(")", "\)")
    escaped_message = escaped_message.replace("=", "\=")
    return escaped_message


def phoneToPlain(phone):
    plainphone = phone.replace("(","")
    plainphone = plainphone.replace(")", "")
    plainphone = plainphone.replace("-", "")
    plainphone = plainphone.replace(" ", "")
    return plainphone


def retIntIf0(num):
    num = str(int(num)) if int(num) == float(num) else str(num)
    return num


def statusIdToText(status_id):
    statusMatrix = { "0": "Новый",
                     "2": "Получен",
                     "3": "Обрабатывается",
                     "4": "Обработан",
                     "6": "Продажа",
                     "7": "Отказ"
                     }
    return statusMatrix[status_id]


def update_order_status(order_data, status_code):
    order_data["statusID"] = str(status_code)
    orders_array = []
    orders_array.append(order_data)
    r = requests.post(TABLETKI_URL, auth=(TABLETKIUA_API_USERNAME, TABLETKIUA_API_PASSWORD), json=orders_array)


def check_orders(status_code):
    print("Retrieve orders...")
    r = requests.get(TABLETKI_URL + "/" + TABLETKIUA_SN + "/" + str(status_code), auth=(TABLETKIUA_API_USERNAME, TABLETKIUA_API_PASSWORD))
    orders = r.json()

    if (len(orders) > 0):
        print("Received " + str(len(orders)) + " orders...")
    else:
        print("No new orders...")

    for order in orders:
        update_order_status(order_data = order, status_code=2)
        update_order_status(order_data = order, status_code=3)

        customer_phone = phoneToPlain(order['customerPhone'])
        order_created = order['dateTimeCreated'].replace("T", " ")
        order_status_id = "3"
        order_status = statusIdToText(order_status_id)
        order_id = str(order['code'])
        ordered_items = order['rows']

        message_body = []
        message_body.append("*Получен новый заказ\!*")
        message_body.append("ID заказа: *" + order_id + "*")
        message_body.append("Создан: *" + order_created + "*")
        message_body.append("Статус: *" + order_status + "*")
        message_body.append("Телефон клиента: *" + customer_phone + "*")
        message_body.append("Товары в заказе:")

        for item in ordered_items:
            item_name = item['goodsName']
            item_price = retIntIf0(item['price'])
            item_qty = retIntIf0(item['qty'])
            message_body.append("*" + item_name + "*, *" + item_qty + "*, *" + item_price + "*")

        message = "\n".join(message_body)
        send_message(message)


def check_online():
    print('Check run at: %s' % datetime.now())
    check_orders(status_code=0)


if __name__ == "__main__":
    check_online()
    scheduler = BlockingScheduler(timezone="Europe/Kiev")
    scheduler.add_job(check_online,  'interval', seconds=300)
    scheduler.start()
