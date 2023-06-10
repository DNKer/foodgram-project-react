# Foodgram. Ваш «Продуктовый помошник».

## [Проект публикаций кулирантых рецептов, позволяющий облегчить труд хозяйке, сформировав список необходимых продуктов для похода в магазин.](http://foodgrams.ddns.net "перейти на сайт.")

![workflow](https://github.com/DNKer/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master&event=push)

## Описание.

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

<img src="frontend\src\images\young-woman-26345588.png" alt="drawing" width="500"/>

## Технологии.
[![Python](https://img.shields.io/badge/-Python-464646?style=plastic&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=plastic&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=plastic&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=plastic&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=plastic&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=plastic&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=plastic&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=plastic&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=plastic&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=plastic&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=plastic&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)

#### Что могут делать неавторизованные пользователи
- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.
#### Что могут делать авторизованные пользователи
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.
#### Что может делать администратор
Администратор обладает всеми правами авторизованного пользователя.
Плюс к этому он может:
- изменять пароль любого пользователя,
- создавать/блокировать/удалять аккаунты пользователей,
- редактировать/удалять любые рецепты,
- добавлять/удалять/редактировать ингредиенты.
- добавлять/удалять/редактировать теги.

Все эти функции реализованы в стандартной админ-панели Django.

**IP: 146.185.209.153 или foodgrams.ddns.net**
**логин: dnk@ya.ru**
**пароль: 87054Kc**

#### Запуск проекта в контейнерах

- Клонирование удаленного репозитория
```bash
git clone git@github.com:dnker/foodgram-project-react.git
cd infra
```
- В директории /infra создайте файл .env, с переменными окружения, используя образец [.env.example](infra/.env.example)
- Сборка и развертывание контейнеров
```bash
docker-compose up -d --build
```
- Выполните миграции, соберите статику, создайте суперпользователя
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py createsuperuser
```
- Наполните базу данных ингредиентами и тегами
```bash
docker-compose exec backend python manage.py load_data
```
- или наполните базу тестовыми данными (включают посты и пользователей)
```bash
cat dump.json | sudo docker exec -i <ID контейнера> python manage.py loaddata --format=json -e contenttypes -e auth.Permission -
```
- Стандартная админ-панель Django доступна по адресу [`https://localhost/admin/`](https://localhost/admin/)
- Документация к проекту доступна по адресу [`https://localhost/api/docs/`](`https://localhost/api/docs/`)

#### Запуск API проекта в dev-режиме

- Клонирование удаленного репозитория (см. выше)
- Создание виртуального окружения и установка зависимостей
```bash
cd backend
python -m venv venv
. venv/Scripts/activate (windows)
. venv/bin/activate (linux)
pip install --upgade pip
pip install -r -requirements.txt
```
- Примените миграции и соберите статику
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```
- Наполнение базы данных ингредиентами и тегами
```bash
python manage.py load_data
python manage.py load_tags
```

- Запуск сервера
```bash
python manage.py runserver 
```