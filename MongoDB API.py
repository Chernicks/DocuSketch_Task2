from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log

app = Flask(__name__)

# В этом классе будут прописаны все взаимодействия с MongoDB
class MongoAPI:
    def __init__(self, data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        # По этому адресу мы сможем подключаться к MongDB через Compass 
        # self.client = MongoClient("mongodb://localhost:27017/")
        # А по этому адресу БД будет связываться с приложением
        self.client = MongoClient("mongodb://mymongo:27017/")

        # Настраиваем взаимодействие с MongoDB, указываем название БД и коллекции
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    # Этот метод будет отвечать за прочтение документов из коллекции по запросу
    # Тут мы переформируем данные в тип Словарь. "_id" нужен только для внутрненних нужд Mongo
    def read(self):
        log.info('Reading All Data')
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    # Этот метод отвечает за добавление документов в коллекцию по запросу.
    # Метод insert_one позволяет вставлять по одному документу за раз, а insert_many() для множества
    def write(self, data):
        log.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    # Этот метод отвечает за изменение документа в БД.
    # Тут метод update_one () изменяет один, при желании можно изменить на update_many ()
    def update(self):
        log.info('Updating Data')
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    # При желании можем добавить метод удаления документа из БД
    # def delete(self, data):
    #     log.info('Deleting Data')
    #     filt = data['Filter']
    #     response = self.collection.delete_one(filt)
    #     output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
    #     return output

# Инициализируем точку входа, так мы сможем проверить что сервер работает
# При запросе корневого пути "http://127.0.0.1:8080/" будет выдан ответ {"Status": "UP"}
@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')

# Реализация метода R из CRUD API. По правильному JSON запросу метода GET читаются данные из коллекции
@app.route('/mongodb', methods=['GET'])
def mongo_read():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

# Реализация метода C из CRUD API. По правильному JSON запросу метода POST записываются данные в коллекцию
@app.route('/mongodb', methods=['POST'])
def mongo_write():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.write(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

# Реализация метода U из CRUD API. По правильному JSON запросу метода UPDATE обновляются данные в коллекции
@app.route('/mongodb', methods=['PUT'])
def mongo_update():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.update()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

# Реализация метода D из CRUD API. По правильному JSON запросу метода DELETE удаляются данные в коллекции
# @app.route('/mongodb', methods=['DELETE'])
# def mongo_delete():
#     data = request.json
#     if data is None or data == {} or 'Filter' not in data:
#         return Response(response=json.dumps({"Error": "Please provide connection information"}),
#                         status=400,
#                         mimetype='application/json')
#     obj1 = MongoAPI(data)
#     response = obj1.delete(data)
#     return Response(response=json.dumps(response),
#                     status=200,
#                     mimetype='application/json')

# Запускаем, в случае если это главный файл, на локальном адресе и порту 8080
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')