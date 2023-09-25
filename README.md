# Mailing service :e-mail:

:incoming_envelope: Сервис для создания периодических рассылок для выбранных клиентов.
Также в сервисе присутствует блог - новостная лента с информационными или развлекательными сообщениями,
отображаемыми пользователю сервиса. 

Сервис использует инструмент Unix-система, для выполнения различных заданий - **Cron**, 
а также **Redis** -  NoSQL базу данных для выполнения кеширования некоторых элементов сервиса.


### Шаги для корректной установки сервиса :feet:
1. Склонировать проект
2. Проверить наличие и установить при необходимости программы **Cron** и **Redis**
3. Установить виртуальное окружение для проекта и активировать его
4. Установить зависимости в venv ```pip install -r requirements.txt```
5. Создать нужную базу данных в **postgres**
6. Переименовать файл **.env.sample** (в корне проекта) на **.env**
7. В файл .env внести и/или изменить данные настроек конфигурации проекта
8. Запустить команду ```python manage.py migrate```, чтобы применить миграции и создать нужные таблицы и связи в базе данных
9. Запустить команду ```python manage.py create_superuser``` для создания суперпользователя (админа)
10. Запустить команду ```python manage.py create_manager``` для создания группы менеджеров. Далее можно в административной панели
    или через консоль добавить надлежащих пользователей в эту группу. Права группы менеджеров будут описаны ниже
11. Ввести команду ```python manage.py loaddata data.json``` (при необходимости) для заполнения базы данных тестовыми данными
12. Запустить сайт ```python manage.py runserver```
13. Для старта выполнения периодических задач ввести команду ```python manage.py crontab add```

### Функционал менеджера :necktie:
+ Может просматривать любые рассылки.
+ Может просматривать список пользователей сервиса.
+ Может блокировать пользователей сервиса.
+ Может отключать рассылки.
+ Не может редактировать рассылки.
+ Не может управлять списком рассылок.
+ Не может изменять рассылки и сообщения.

#### Пример домашней страницы сайта
![Домашняя страница](http://joxi.net/82Qo4XzI4znLQr.jpg)

#### Пример страницы со списком рассылок
![Список рассылок](http://joxi.net/Q2KJqZMUgoKV4m.jpg)

#### Пример страницы со списком пользователей
![Пользователи](http://joxi.net/82318YQHwbvNar.jpg)


:shipit:
