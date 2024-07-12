from django.db.models import CharField, BooleanField, DateTimeField

from shared import CreatedBaseModel


class Customer(CreatedBaseModel):
        first_name = CharField(max_length=30, null=True)
        username = CharField(max_length=30, unique=True)
        is_blocked = BooleanField(db_default=False)
        last_activity = DateTimeField(auto_now_add=True)


# order da customer field buladi













