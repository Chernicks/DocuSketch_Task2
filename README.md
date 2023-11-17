<pre>
ЗАДАНИЕ
Создать docker-compose.yml разворачивающий приложение на python с простой реализацией REST API. Решение должно состоять из двух контейнеров:
а) Любая NoSQL DB.
б) Приложение на python, с использованием Flask, которое слушает на порту 8080 и принимает только методы GET, POST, PUT.
в) Создаем значение ключ=значение, изменяем ключ=новое_значение, читаем значение ключа.
г) Вновь созданные объекты должны создаваться, изменяться и читаться из NoSQL DB.
***
ЗАПУСК И ТЕСТИРОВАНИЕ
Запустить приложение можно так
docker-compose up
При переходе по адресу http://127.0.0.1:8080/ получим ответ {"Status": "UP"}
Проверять можно в программе MongoDB Compass подключившись по адресу mongodb://localhost:27017/
Воспользуемся программой Postman для проверки остальных запросов
Запросы будут отправляться по адресу http://127.0.0.1:8080/mongodb
Добавим новый документ в коллекцию
Для этого сформируем запрос с использованием метода POST
В body сформируем raw JSON с содержимым:
{
  "database": "IshmeetDB",
  "collection": "people",
  "Document": {
    "First_Name": "Jhon",
    "Age": 50
  }
}
В ответ получим
{
    "Document_ID": "65572679bb36b430fec14ddc",
    "Status": "Successfully Inserted"
}
Выведем содержимое колеекции
Для этого сформируем запрос с использованием метода GET
В body сформируем raw JSON с содержимым:
{
  "database": "IshmeetDB",
  "collection": "people"
}
В ответ получим
[
    {
        "Age": 50,
        "First_Name": "Jhon"
    }
]
Изменим документ колеекции
Для этого сформируем запрос с использованием метода PUT
В body сформируем raw JSON с содержимым:
{
  "database": "IshmeetDB",
  "collection": "people",
  "Filter": {
    "First_Name": "Jhon"
  },
  "DataToBeUpdated": {
    "Last_Name": "Bindra",
    "Age": 26
  }
}
В ответ получим
{
    "Status": "Successfully Updated"
}
УДАЛЕНИЕ ЗАКОММЕНТИРОВАНО, НО ЕСЛИ ПОНАДОБИТСЯ:
Удалим документ колеекции
Для этого сформируем запрос с использованием метода DELETE
В body сформируем raw JSON с содержимым:

  "database": "IshmeetDB",
  "collection": "people",
  "Filter": {
    "First_Name": "Jhon"
  }
}
</pre>
