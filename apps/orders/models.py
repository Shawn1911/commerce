from django.db import models

from shared import CreatedBaseModel


# Create your models here.


class PromoCode(CreatedBaseModel):
    class Type(models.TextChoices):
        PERCENT = 'percent', 'Percent'
        FREE = 'free', 'Free'

    active = models.BooleanField(default=True)
    code = models.CharField(max_length=7, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    limit = models.IntegerField()
    remaining_quantity = models.IntegerField()
    promo_type = models.CharField(max_length=255, choices=Type.choices, default=Type.FREE)
    percent = models.IntegerField(default=0)
    user_quantity = models.IntegerField()

