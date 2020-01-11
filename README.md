# Screen Docs Панель администратора

## Как развернуть образ
##### Клонировать проект
```sh
git clone git@bitbucket.org:spotappteam/spotdocker.git
cd spotdocker/
```
##### Файл настроек Django
- В папке sdocs/settings нужно скопировать файл .env.example в .env
- Затем сгенерировать SECRET_KEY и записать (его можно сгенерировать [здесь](https://djecrety.ir/))
- В CORS_ORIGIN_WHITELIST записать хост фронта
##### Docker Compose
- Скопировать docker-compose.yml.example в docker-compose.yml
- В нём в обоих `environment` заполнить данные БД, а так же указать необходимые порты
- И запустить файл
```sh
docker-compose up -d --build
```