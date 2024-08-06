# ToDoList_Django 📝 - API для введения дел, написанная на фреймворке Django

## С помощью API вы можете:
* регистрироваться и авторизовываться;
* создавать список задач;
* удалять задачу из списка;
* обновлять задачу;
* давать/отнимать/обновлять право на вашу задачу (чтение, обновление) другому пользователю
* отправлять запрос на дружбу и хранить список друзей, у которых будет доступ к вашим задачам
* просматривать список задач, доступные вам от других пользователей

## Необходимые шаги для запуска проекта:
1. Скопировать репозиторий (SSH ключ):
```py
git clone git@github.com:dinarius1/TodoListBot2.git
```
2. Создать и активировать виртуальное окружение:
```py
python3 -m venv venv
. venv/bin/activate
```
3. Установить необходимые библиотеки:
```py
pip install -r requirements.txt
```
4. Создать базу данных
```
\psql
create database todolist;
\q
```
6. Создать .env и прописать следующие пункты ниже. Заполнить пустые параметры.
- **EMAIL_HOST_USER** - брала в качества хоста mail.ru
- **EMAIL_HOST_PASSWORD** - использовала пароль для внешних приложений
```py
SECRET_KEY=
DEBUG=1
ALLOWED_HOST=127.0.0.1

DB_HOST =127.0.0.1
DB_NAME=todolist
DB_USER=
DB_PASSWORD=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

SITE_ID=1
LINK=http://127.0.0.1:8000/
```
5. Провести миграцию
```py
python manage.py makemigrations
python manage.py migrate        
```
7. Запустить проект локально:
```py
python manage.py runserver      
```
8. Запустить Celery:
```py
celery -A config worker --loglevel=info      
```
