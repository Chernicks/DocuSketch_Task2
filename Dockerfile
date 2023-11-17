# Выбираем стандартный образ
FROM alpine

# Формируем слои установки
RUN apk add --no-cache python3-dev && apk add cmd:pip3 && pip3 install --upgrade pip

# Создадим рабочую директорию
WORKDIR /app

# Добавим файл с требуемыми библиотеками
COPY /requirements.txt /app

# Установим все необходимые библиотеки
RUN pip3 install -r requirements.txt

# Скопируем в рабочую папку главный свой скрипт
COPY ["MongoDB API.py", "/app"]

# Доступно приложение будет на этом порту
EXPOSE 8080

# Указываем команду запуска
ENTRYPOINT [ "python3" ]

# М что бдует запускаться этой командой
CMD ["MongoDB API.py"]