#!/bin/bash

./manage.py makemigrations
./manage.py migrate

echo "from users.models import User; User.objects.create_superuser('admin@admin.com', '1')" | python manage.py shell

python manage.py loaddata service country currency languages shop_category plans plan_pricing quotas plan_quotas