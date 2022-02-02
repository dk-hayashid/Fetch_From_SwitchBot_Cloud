from csv import writer
import datetime
import pytz
import requests
import json
from tqdm import tqdm


def main():

    headers = {
        "Authorization": "",  # ここにSwitchBotアプリで発行したAPIトークンを貼る
        "content-type": "application/json"
    }

    # デバイス名→デバイスidの辞書を用意
    with open('devicename2id.json', 'r') as f:
        devicename2id = json.load(f)

    now = datetime.datetime.now(pytz.timezone(
        'Asia/Tokyo')).strftime("%Y年%m月%d日%H時%M分")
    measurement = {
        "temperature": [now],
        "humidity": [now]
    }

    for id_ in tqdm(devicename2id.values()):
        response = requests.get(
            f"https://api.switch-bot.com/v1.0/devices/{id_}/status", headers=headers)
        for feature, listdata in measurement.items():
            data = response.json()['body'][feature]
            listdata.append(data)

    for feature, listdata in measurement.items():
        with open(f'measurement/{feature}.csv', 'a') as f:
            writer_object = writer(f)
            writer_object.writerow(listdata)


if __name__ == "__main__":
    main()
