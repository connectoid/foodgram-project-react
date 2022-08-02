Foodgram
Cервис для публикаций и обмена рецептами.

Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачивать список покупок. Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других пользователей.

Foodgram Workflow

Стек технологий
Python 3.9.7, Django 3.2.7, Django REST Framework 3.12, PostgresQL, Docker, Yandex.Cloud.

Установка
Для запуска локально, создайте файл .env в директории /backend/ с содержанием:

SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
DEBUG=False
ALLOWED_HOSTS=*,или,ваши,хосты,через,запятые,без,пробелов
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль_к_базе_данных_на_ваш_выбор
DB_HOST=bd
DB_PORT=5432
Установка Docker
Для запуска проекта вам потребуется установить Docker и docker-compose.

Для установки на ubuntu выполните следующие команды:

sudo apt install docker docker-compose
Про установку на других операционных системах вы можете прочитать в документации и про установку docker-compose.

Установка проекта на сервер
Скопируйте файлы из папки /server/ на ваш сервер и .env файл из директории /backend/:
scp -r data/ <username>@<server_ip>:/home/<username>/
scp backend/.env <username>@<server_ip>:/home/<username>/
Зайдите на сервер и настройте server_name в конфиге nginx на ваше доменное имя:
vim nginx.conf
Настройка проекта
Запустите docker compose:
docker-compose up -d
Примените миграции:
docker-compose exec backend python manage.py migrate
Заполните базу начальными данными (необязательно):
docker-compose exec backend python manange.py loaddata data/fixtures.json
Создайте администратора:
docker-compose exec backend python manage.py createsuperuser
Соберите статику:
docker-compose exec backend python manage.py collectstatic
Как импортировать данные из своего csv файла?
Для начала убедитесь, что первая строчка вашего csv файла совпадает с названиями полей в модели. Если на первой строчке нет названия полей или они неправильные, исправьте, прежде чем приступать к импортированию.

Импортирование с помощью скрипта
Заходим в shell:
docker-compose exec backend python manage.py shell
Импортируем нужные модели:
from recipes.models import Ingredient, Tags
Импортируем скрипт:
from scripts.import_data import create_models
Запускаем скрипт с тремя параметрами:
file_path — путь до вашего csv файла,

model — класс модели из импортированных ранее,

print_errors — нужно ли распечатать каждую ошибку подробно? (True or False)

Пример:

create_models('../data/ingredients.csv', Ingredient, True)
Сайт
Сайт доступен по ссылке: http://51.250.21.59/

Документация к API
Документация доступна по адресу: http://51.250.21.59/api/docs/
