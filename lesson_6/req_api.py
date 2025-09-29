import requests
import json


def get_pic_fox(num: int) -> list[str]:
    res = []
    for _ in range(num):
        answer = requests.get("https://randomfox.ca/floof").json()
        res.append(answer["image"])
    return res


def get_pic_duck() -> str:
    """ Ооооооочень медленное api... моего терпения не хватает

    :return:
    """
    answer = requests.get("https://random-d.uk/api/random").json()
    return answer["url"]


def get_pic_duck2() -> str:
    """ т.к. api с утками тормозит, то возвращаем лису...

    :return:
    """
    answer = requests.get("https://randomfox.ca/floof").json()
    return answer["image"]


def get_weather(city):
    """
    синхронная функция получения погоды
    """
    url = f'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}
    res = requests.get(url, params).json()
    _dict = {"main": res["weather"][0]["main"], "temp": res["main"]["temp"], "wind": res["wind"]["speed"], "humidity": res["main"]["humidity"], "pressure":res["main"]["pressure"]}
    return _dict
    #return f'main:{res["weather"][0]["main"]}, temp:{res["main"]["temp"]}, wind: {res["wind"]["speed"]}, humidity:{res["main"]["humidity"]}, pressure:{res["main"]["pressure"]}'
   # return f'main:{res["weather"][0]["main"]}, temp:{res["main"]["temp"]}, wind: {res["wind"]["speed"]}'

