#!/bin/bash
# Перед запуском скрипта необходимо удалить схему public вручную и заново создать её(со всеми правами)
# Запустить скрипт из папки api:
# sh scripts/start/reinit.sh
#
# Удалить все файлы миграций (опционально)
find ./apps/ -path '*/migrations/*.py' -not -name '__init__.py' -delete;
# Запустить миграции
python manage.py makemigrations;
python manage.py migrate;
# Создать суперпользователя(укажите email и пароль, которые используете в тестовой среде)
echo "from apps.users.models import User; User.objects.create_superuser('admin@mail.ru', '1234')" | python manage.py shell;
# Или вручную python manage.py createsuperuser
# Заполнить базу init данными
python manage.py loaddata fixtures.json;
python manage.py shell < scripts/seeders/admin_panel_init_data.py;