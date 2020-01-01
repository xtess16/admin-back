#!/bin/bash
#
python3 -m venv spotenv;
. spotenv/bin/activate;
python -m pip install --upgrade pip;
pip install --upgrade wheel;
pip install setuptools --upgrade;
pip install -r requirements.txt;
python manage.py migrate;
echo "from apps.users.models import User; User.objects.create_superuser('admin@mail.ru', '1234')" | python manage.py shell;
python manage.py loaddata fixtures.json;
python manage.py shell < scripts/seeders/admin_panel_init_data.py;
# gitusername и gituseremail
#