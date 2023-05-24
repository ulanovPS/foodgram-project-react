# **_Grocery_Assistant_**

Дипломный проект — сайт Foodgram, «Продуктовый помощник», онлайн-сервис и API.
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### _Развернуть проект на удаленном сервере:_

**_Клонировать репозиторий:_**

```
git@github.com:ulanovPS/foodgram-project-react.git
```

**_Установить на сервере Docker, Docker Compose:_**

```
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose
```

### Технологии проекта

Python 3.7-slim
Django 3.2
Django Rest framework 3.12.4
PostgreSQL 2.8.6
Gunicorn 20.0.4
**_Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra (команды выполнять находясь в папке infra):_**

```
scp docker-compose.yml nginx.conf username@IP:/home/username/

# username - имя пользователя на сервере
# IP - публичный IP сервера
```

**_Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:_**

```
SECRET_KEY              - секретный ключ Django проекта
DOCKER_PASSWORD         - пароль от Docker Hub
DOCKER_USERNAME         - логин Docker Hub
HOST                    - публичный IP сервера
USER                    - имя пользователя на сервере
PASSPHRASE              - *если ssh-ключ защищен паролем
SSH_KEY                 - приватный ssh-ключ
TELEGRAM_TO             - ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          - токен бота, посылающего сообщение

DB_ENGINE               - django.db.backends.postgresql
DB_NAME                 - postgres
POSTGRES_USER           - postgres
POSTGRES_PASSWORD       - postgres
DB_HOST                 - db
DB_PORT                 - 5432 (порт по умолчанию)
```

**_Создать и запустить контейнеры Docker, выполнить команду на сервере (версии команд "docker compose" или "docker-compose" отличаются в зависимости от установленной версии Docker Compose):**_

```
sudo docker compose up -d
```

**_Выполнить миграции:_**

```
sudo docker compose exec backend python manage.py migrate
```

**_Собрать статику:_**

```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

**_Наполнить базу данных содержимым из файла ingredients.json:_**

```
sudo docker compose exec backend python manage.py loaddata ingredients.json
```

**_Создать суперпользователя:_**

```
sudo docker compose exec backend python manage.py createsuperuser
```

**_Для остановки контейнеров Docker:_**

```
sudo docker compose down -v      - с их удалением
sudo docker compose stop         - без удаления
```

### После каждого обновления репозитория (push в ветку master) будет происходить

1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
2. Сборка и доставка докер-образов frontend и backend на Docker Hub
3. Разворачивание проекта на удаленном сервере
4. Отправка сообщения в Telegram в случае успеха

### IP адрес проекта и пользователи

IP - 158.160.21.241

username=p.s.ulanov
email=p.s.ulanov@gmail.com
pas=pavel

user_name=vlasova_zin
email=vlasova_zin@bk.ru
pas=pavel

### Автор

Уланов Павел C