from flask import Flask, request
import requests
from dotenv import load_dotenv
import os
import csv
from os.path import join, dirname
from yookassa import Configuration, Payment
import json
from time import gmtime, strftime
import telebot, time
numbers=list()
requesttg=list()
timing=list()
imya=list()
payment=list()
app = Flask(__name__)
def create_invoice_first(chat_id):
    Configuration.account_id = get_from_env("ID")
    Configuration.secret_key = get_from_env("PAYMENT_TOKEN")
    payment = Payment.create({
        "amount": {
            "value": "1000",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.google.com"
        },
        "capture": True,
        "description": "Заказ №1",
        "metadata": {"chat_id": chat_id}
    })
    return payment.confirmation.confirmation_url
def create_invoice_second(chat_id):
    Configuration.account_id = get_from_env("ID")
    Configuration.secret_key = get_from_env("PAYMENT_TOKEN")
    payment = Payment.create({
        "amount": {
            "value": "2000",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.google.com"
        },
        "capture": True,
        "description": "Заказ №1",
        "metadata": {"chat_id": chat_id}
    })
    return payment.confirmation.confirmation_url
def create_invoice_third(chat_id):
    Configuration.account_id = get_from_env("ID")
    Configuration.secret_key = get_from_env("PAYMENT_TOKEN")
    payment = Payment.create({
        "amount": {
            "value": "3000",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.google.com"
        },
        "capture": True,
        "description": "Заказ №1",
        "metadata": {"chat_id": chat_id}
    })
    return payment.confirmation.confirmation_url
def create_invoice_four(chat_id):
    Configuration.account_id = get_from_env("ID")
    Configuration.secret_key = get_from_env("PAYMENT_TOKEN")
    payment = Payment.create({
        "amount": {
            "value": "4000",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.google.com"
        },
        "capture": True,
        "description": "Заказ №1",
        "metadata": {"chat_id": chat_id}
    })
    return payment.confirmation.confirmation_url
def create_invoice_five(chat_id):
    Configuration.account_id = get_from_env("ID")
    Configuration.secret_key = get_from_env("PAYMENT_TOKEN")
    payment = Payment.create({
        "amount": {
            "value": "5000",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.google.com"
        },
        "capture": True,
        "description": "Заказ №1",
        "metadata": {"chat_id": chat_id}
    })
    return payment.confirmation.confirmation_url
def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)  # возвращен серкетный токен (или ключ к платежной системе)
def send_message(chat_id, text):
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)
def send_pay_button(chat_id, text):
    if len(requesttg)<=10:
        invoice_url = create_invoice_first(chat_id)
    elif 10<len(requesttg)<=20:
        invoice_url = create_invoice_second(chat_id)
    elif 20<len(requesttg)<=30:
        invoice_url = create_invoice_third(chat_id)
    elif 30<len(requesttg)<=40:
        invoice_url = create_invoice_four(chat_id)
    elif 40<len(requesttg)<=50:
        invoice_url = create_invoice_five(chat_id)
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text, "reply_markup": json.dumps({"inline_keyboard": [[{
        "text": "Оплатить!",
        "url": f"{invoice_url}"
    }]]})}
    requests.post(url, data=data)
def check_if_successful_payment(request):
    try:
        if request.json["event"] == "payment.succeeded":
            return True
    except KeyError:
        return False
    return False
@app.route('/', methods=["POST"])  # localhost:5000/ - на этот адрес телеграм шлет свои сообщение
def process():
    if check_if_successful_payment(request):
        # Обработка запроса от Юкассы
        print(request.json)
        chat_id = request.json["object"]["metadata"]["chat_id"]
        send_message(chat_id, "Оплата прошла успешно!")
        send_message(chat_id, "Никому не отправляйте его,кроме бота,секретное сообщение,чтобы до конца поддтвердить свой платеж:Zdesdolzhnonytchto-toslozhnoe")
        send_message(chat_id,"Не беспокойтесь,платеж прошел успешно,это нужно для нас,для более детальной отчетности")
    #установка счетчика для суммы платежа и создание массива из айдишников для определения очереди
    elif request.json["message"]['text']=="/start":
        send_message(chat_id=request.json["message"]["chat"]["id"], text="Пожалуйста,отправьте ваш номер телефона в таком формате: +78005553535")
        if request.json["message"]["chat"]["id"] not in requesttg:
            requesttg.append(request.json["message"]["chat"]["id"])
            imya.append(request.json["message"]["chat"]['username'])
    start = 1000 #началаьная оплата
    if 10<len(requesttg)<=20:
        start+=1000
    elif 20<len(requesttg)<=30:
        start+=2000
    elif 30<len(requesttg)<=40:
        start+=3000
    elif 40<len(requesttg)<=50:
        start+=4000
    elif request.json["message"]['text'][0]=='+' and len(request.json["message"]['text'])==12 and request.json["message"]['text'] not in numbers:
        try:
            numbers.append(request.json["message"]['text'])
            start=str(start)
            length=str(len(requesttg))
            send_message(chat_id=request.json["message"]["chat"]["id"], text='Вы в очереди под номером '+length+' Теущий ценник '+start)
            time.sleep(1)
            send_message(chat_id=request.json["message"]["chat"]["id"],text="Отправьте боту '1',если все еще хотите совершить оплату")
        except KeyError:
            print()
    elif request.json["message"]['text']=="1" :
        # Обработка запроса от Телеграм
        chat_id = request.json["message"]["chat"]["id"]
        send_pay_button(chat_id=chat_id, text="Нажав на кнопку,перейдите пожалуйста по ссылке")
    elif request.json["message"]['text']=="Zdesdolzhnonytchto-toslozhnoe":
        send_message(chat_id=request.json["message"]["chat"]["id"], text="Спасибо огромное!Вы нам очень помогли")
        timing.append(request.json["message"]["date"])
    with open("infa.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow(["Имя", "Номер", "айди","дата и время оплаты(если есть)"])
        for i in range(len(requesttg)):
            file_writer.writerow([str(imya[i]), str(numbers[i]), str(requesttg[i]), str(timing[i])])
    return {"ok": False}
if __name__ == '__main__':
    app.run()
