import random
import string
from decimal import Decimal


def translate_message(language):  # noqa
    data = {
        'en': 'Activate your account',
        'ru': 'Активируйте вашу учетную запись',
        'uz': 'Hisobingizni faollashtiring'
    }

    return data.get(language, 'Activate your account')


def unique_code():
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))


def check_data(data, obj):
    for key, value in data.items():
        if isinstance(getattr(obj, key), Decimal):
            obj_data = f"{getattr(obj, key):.2f}"
        else:
            obj_data = getattr(obj, key)
        if value != obj_data:
            print(f"{value} {obj.key} ga teng emas!")
            return False
    else:
        return True
