# Финальный проект - Продуктовый помощник

## Адрес:

* http://158.160.57.173/

Данный проект даст вам возможность получить или поделиться кулинарным опытом.

### Функционал

* Для неавторизованных пользователей доступен весь контент в целях ознакомления
* Для публикации и другого встроенного функционала требуется пройти авторизацию на сайте
* Аутентификация происходит на встроенном TokenAuthentication
* Авторизованным пользователям доступно:
    * Публикация собственных рецептов;
    * Добавление рецептов, опубликованных на сайте, в Избранное и список покупок
    * Скачивание файла списка своих покупок вида "Ананасовый сок(мл) - 500 ..."
    * Редактирование и удаление своих рецептов
    * Редактирование и удаление своего аккаунта

### Документация

После запуска проекта для просмотра документации и доступных эндпоинтов [http://158.160.57.173/api/docs/](http://158.160.57.173/api/docs/).

### Технологии
* [Python 3.10+](https://www.python.org/)
* [Django 4.2](https://www.djangoproject.com/)
* [Django Rest Framework 3.14.0](https://www.django-rest-framework.org)
* [Djoser 2.1.0](https://djoser.readthedocs.io/en/latest/getting_started.html)

### Шаблон наполнения файла .env


- указываем, с какой БД работаем:
``` DB_ENGINE=django.db.backends.postgresql ```
- имя базы данных:
``` DB_NAME= ```
- логин для подключения к базе данных:
``` POSTGRES_USER= ```
- пароль для подключения к БД (установите свой):
``` POSTGRES_PASSWORD= ```
- название сервиса (контейнера):
``` DB_HOST= ```
-порт для подключения к БД:
``` DB_PORT= ```

### Как запустить проект

- Клонируйте репозиторий и перейдите в него в командной строке:
``` git clone <ссылка на репозиторий> ``` 
``` cd foodgram-project-react ```
- Перейдите в папку с проектом:
``` cd backend ```
- Cоздайте и активируйте виртуальное окружение:
``` python3 -m venv venv ``
``` . venv/bin/activate ```
``` python3 -m pip install --upgrade pip ```
- Установите зависимости из файла requirements.txt:
``` pip install -r requirements.txt ```
- Перейдите в папку с файлом docker-compose.yaml:
``` cd infra ```
- Разверните контейнеры:
``` docker-compose up -d --build ```
- Выполните миграции:
``` docker-compose exec web python manage.py migrate ```
- Создайте суперпользователя:
``` docker-compose exec web python manage.py createsuperuser ```
- Соберите статику:
``` docker-compose exec web python manage.py collectstatic --no-input ```
- Создайте дамп (резервную копию) базы:
``` docker-compose exec web python manage.py dumpdata > fixtures.json ```
- Заполните базу начальными данными:
```docker-compose exec web python manage.py loaddata fixtures.json ```

### Примеры запросов

Все запросы происходят в формате ```JSON```

Вы можете получить список всех рецептов перейдя по адресу
``` GET .../api/recipes/```
На что получите примерно такой ответ:
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "Ezu4x3Xz",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": false,
      "is_in_shopping_cart": false,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

Пользователи, на которых захотите подписаться, дабы узнать о новых опубликованных рецептах, ```POST .../api/users/{id}/subscribe/```: 

```
{
  "email": "user@example.com",
  "id": 0,
  "username": "kALiQGMrIUWd-CQcSUsbaXDMHWFDAfhmVCUyuEaCjLQY0Q4uAOZt7FnmSoHVN7-zYQW4s+nFHM0IKLsC5Paq@pptPVohXirz",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0
}
```

А так же просмотреть список ингредиентов для ваших новых рецептов ```GET .../api/ingredients/```:

```
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```

### Автор:
[Тимур](https://github.com/TimurMahmudov)


Администратор:

```
Логин: foodgram_exormalik
Пароль: tGotFM18103
```
