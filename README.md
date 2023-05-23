<h1>Проект YaMDb собирает отзывы пользователей на различные произведения.<h1>

<h2>
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). 
Пользователи могут оставлять комментарии к отзывам.
<h2>

<h2>Стек технологий<h2>

* Python
* Django REST API
* библиотека Simple JWT - работа с JWT-токеном
* Postgres
* Docker

### Как запустить проект:

- Склонируйте репозитрий на свой компьютер

- Создайте `.env` файл в директории `infra/`, в котором должны содержаться следующие переменные:
    >DB_ENGINE=django.db.backends.postgresql\
    >DB_NAME= # название БД\ 
    >POSTGRES_USER= # ваше имя пользователя\
    >POSTGRES_PASSWORD= # пароль для доступа к БД\
    >DB_HOST=db\
    >DB_PORT=5432\

- Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

- Запустите docker-compose:
```
docker-compose up -d --build
```

- Соберите файлы статики, и запустите миграции командами:
```
docker-compose exec web python3 manage.py makemigrations
```
```
docker-compose exec web python3 manage.py migrate
```
```
docker-compose exec web python3 manage.py collectstatic --no-input
```

- Создайте суперпользователя командой:
```
docker-compose exec web python3 manage.py createsuperuser
```

- Команда по загрузке файла fixtures в БД
```
docker-compose exec web python3 manage.py dumpdata > fixtures.json
```

- Остановить можно командой:
```
docker-compose down -v
```


### Ресурсы API YaMDb

* Ресурс AUTH: аутентификация.
* Ресурс USERS: пользователи.
* Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
* Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
* Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
* Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
* Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.

Каждый ресурс описан в документации: указаны эндпойнты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.

### Развернутый проект:
http://158.160.24.209/

<h3>Авторы:<h3>
[Таргонский Михаил](https://github.com/mishatar)
[Федорова Виктория](https://github.com/vika301296)
[Мугинов Тимур](https://github.com/timurmuginov)

![yamdb_final](https://github.com/vika301296/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
