import requests
import datetime
import time
from win10toast import ToastNotifier

toaster = ToastNotifier()

url = 'https://rest.coinapi.io/v1/exchangerate/BTC/EUR'
headers = {'X-CoinAPI-Key': '6C7D0D7B-2AE9-4625-ABD9-B58D907D82B9'}
res = requests.get(url, headers=headers)
res = res.json()
act_btc = round(res['rate'], 2)

start_time = time.time()


def get_rounded_per(value):
    if value > act_btc:
        return str(abs(round(100 - (value / act_btc) * 100, 2))) + "%"
    else:
        return str(round(100 - (value / act_btc) * 100, 2)) + "%"


print("\nNotifikácia o hodnote dôjde každých 15 minúť...\n")
print("Aktuálna hodnota BTC je:", act_btc, "€")
print("\nNastavenie limitov pre tento session...\n")
min_notify = round(float(input("Ak BTC klesne pod hodnotu (€): ")), 2)
print("To je pokles o:", get_rounded_per(min_notify))
max_notify = float(input("Ak BTC pôjde nad hodnotu (€): "))
print("To je navýšenie o:", get_rounded_per(max_notify), "\n")

actual_time = datetime.datetime.now()
actual_time = actual_time.strftime("%H:%M:%S")


def load_state():
    btc = 0.00
    response = requests.get(url, headers=headers)
    response = response.json()

    for key in response:
        if key == "rate":
            btc = round(float(response[key]), 2)
        if key == "time":
            response[key] = actual_time
        print(key, "=", response[key], end="\n")
    print()

    toaster.show_toast("Aktuálny stav BTC - " + actual_time, str(btc) + " €")

    if btc < min_notify:
        toaster.show_toast("Upozornenie na limit", "Bitcoin klesol pod vašu stanovenú hodnotu !")
    elif btc > max_notify:
        toaster.show_toast("Upozornenie na limit", "Bitcoin je nad vašou stanovenou hodnotou !")


while True:
    load_state()
    time.sleep((60 * 15) - (time.time() - start_time) % (60 * 15))
