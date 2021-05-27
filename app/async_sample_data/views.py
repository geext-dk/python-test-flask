from app.async_sample_data import async_sample_data
from app.models import SampleData

import asyncio
import json
from urllib.request import urlopen
from flask import request, g
import time

# Здесь используется параметр timeout функции urlopen, чтобы прервать исполнение.
# 
# Не нашел решения, которое позволяет остановить выполнение Task (или даже Thread), если функция
# этого не поддерживает через параметр. При использовании asyncio.wait_for с timeout выполнение хоть и передается
# вызывающему методу, сам вызов urlopen().read() не останавливается. В итоге вызов asyncio.run не дает
# отправить ответ на запрос, пока не завершится вызов urlopen().read(). 
async def http_get_async(url):
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, lambda: urlopen(url, timeout=2).read())

        return json.loads(result.decode('utf-8'))
    except:
        return []

async def get_sample_data_async():
    # Обернуть все корутины в Task, чтобы они выполнялись одновременно
    # Запросы выполняются "самого в себя". Чтобы это заработало, был добавлен флаг threaded=True
    # в метод app.run() (start.py) иначе по умолчанию приложение выполняется в одном потоке
    task1 = asyncio.create_task(http_get_async(request.base_url + "1"))
    task2 = asyncio.create_task(http_get_async(request.base_url + "2"))
    task3 = asyncio.create_task(http_get_async(request.base_url + "3"))
    
    # Ждем выполнения всех задач...
    (resp1, resp2, resp3) = await asyncio.gather(task1, task2, task3)
    
    all_data = resp1 + resp2 + resp3

    # сортировка по ID
    all_data.sort(key=lambda x: x["id"])

    return json.dumps(all_data)

# метод получения SampleData из всех трех источников (БД и двух JSON-файлов)(
# flask не поддерживает async/await
# (только с помощью дополнительного расширения async, но я не уверен, можно ли его использовать)
# + в документации советуется в таком случае использовать Quart
@async_sample_data.route("/sample-data", methods=["GET"])
def get_sample_data():
    return asyncio.run(get_sample_data_async())

# метод получения SampleData из БД
@async_sample_data.route("/sample-data1", methods=["GET"])
def get_sample_data1():
    entities = g.db.query(SampleData).all()
    return json.dumps(list(map(lambda x: { "id": x.id, "name": x.name }, entities)))

# метод получения SampleData из первого JSON-файла
# для демонстрации возвращает результат только через 10 секунд 
@async_sample_data.route("/sample-data2", methods=["GET"])
def get_sample_data2():
    time.sleep(10)
    with open("sample_data2.json") as f:
        return f.read()

# метод получения SampleData из второго JSON-файла
@async_sample_data.route("/sample-data3", methods=["GET"])
def get_sample_data3():
    with open("sample_data3.json") as f:
        return f.read()