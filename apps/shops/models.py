from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, TextChoices, ManyToManyField, ImageField, \
    IntegerField, FloatField, BooleanField, DateTimeField, OneToOneField, URLField, JSONField

from shared import CreatedBaseModel


class PaymentProvider(Model):
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        NOT_EXISTS = 'not_exists', 'Not exists'

    class Type(TextChoices):
        INPLACE = 'inplace', 'Inplace'
        TELEGRAM = 'telegram', 'Telegram'
        WEB = 'web', 'Web'

    title = CharField(max_length=255)
    code = CharField(max_length=255)
    type = CharField(max_length=255, choices=Type.choices)
    status = CharField(max_length=15, choices=Status.choices, db_default=Status.INACTIVE)
    description = TextField(null=True, blank=True)

    class Meta:
        unique_together = [
            ('code', 'type')
        ]


class PaymentField(Model):
    class Type(TextChoices):
        INTEGER = 'integer', 'Integer'
        STRING = 'string', 'String'
        TEXT = 'text', 'Text'

    label = CharField(max_length=255)
    name = CharField(max_length=255, unique=True)
    required = BooleanField()
    type = CharField(max_length=255, choices=Type.choices)
    provider_labels = JSONField()


class DeliveryService(Model):
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        NOT_EXIST = 'not_exists', 'Not exists'

    class Type(TextChoices):
        INTERVAL = 'interval', 'Interval'

    type = CharField(max_length=20, choices=Type.choices, db_default=Type.INTERVAL)
    max_length = IntegerField(null=True, blank=True)
    title = CharField(max_length=255, null=True)
    code = CharField(max_length=255, unique=True)
    status = CharField(max_length=20, choices=Status.choices, db_default=Status.NOT_EXIST)


class DeliveryField(Model):
    class Type(TextChoices):
        STRING = 'string', 'String'
        VIDEO = 'video', 'Video'
        IMAGE = 'image', 'Image'
        TEXT = 'text', 'Text'
        INTEGER = 'integer', 'Integer'

    delivery = ForeignKey('shops.DeliveryService', CASCADE)
    label = CharField(max_length=255, null=True, blank=True)
    name = CharField(max_length=255, null=True, blank=True)
    required = BooleanField(db_default=True, default=True)
    type = CharField(max_length=20, choices=Type.choices)
    value = JSONField(default=dict)


class Country(Model):
    name = CharField(max_length=100)


class Language(Model):
    title = CharField(max_length=50)


class ShopCategory(Model):  # ✅
    name = CharField(max_length=100)


class Currency(Model):
    name = CharField(max_length=100)


class Shop(CreatedBaseModel):
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        IN_ACTIVE = 'inactive', 'Inactive'

    name = CharField(max_length=255)
    phone_number = CharField(max_length=50)
    country = ForeignKey("shops.Country", CASCADE)
    languages = ManyToManyField("shops.Language")
    shop_category = ForeignKey("apps.ShopCategory", CASCADE)
    status = CharField(max_length=8, choices=Status.choices, db_default=Status.ACTIVE)
    currency = ForeignKey("shops.Currency", CASCADE)
    # starts_at
    # ends_at
    has_terminal = BooleanField(db_default=True)
    about_us = TextField(null=True, blank=True)
    facebook = URLField(max_length=255, null=True, blank=True)
    instagram = URLField(max_length=255, null=True, blank=True)
    telegram = URLField(max_length=255, null=True, blank=True)
    email = URLField(max_length=255, null=True, blank=True)
    call_center = CharField(max_length=50, null=True, blank=True)
    address = CharField(max_length=500, null=True, blank=True)
    # favicon_image


''' Model for Telegram message and Channels '''


class TelegramChannel(Model):
    chat = CharField(max_length=255)
    shop = ForeignKey('shops.Shop', CASCADE, related_name='channels')


class Message(Model):
    class FileType(TextChoices):
        TEXT = 'text', 'Text'
        PHOTO = 'photo', 'Photo'
        VIDEO = 'video', 'Video'

    class MessageStatus(TextChoices):
        SENT = 'sent', 'Sent'
        PENDING = 'pending', 'Pending'
        NOT_SENT = 'not_sent', 'Not sent'

    message = CharField(max_length=5000)
    chat = ForeignKey('shops.TelegramChannel', CASCADE, related_name='messages')
    is_scheduled = BooleanField(default=False)
    scheduled_time = DateTimeField(blank=True, null=True)
    file_type = CharField(max_length=20, choices=FileType.choices, db_default=FileType.TEXT)
    status = CharField(max_length=20, choices=MessageStatus.choices, db_default=MessageStatus.PENDING)
    created_at = DateTimeField(auto_now_add=True)


"Create Web Site and Telegram Bot"


class Commerce(Model):
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    name = CharField(max_length=30)
    status = CharField(max_length=8, choices=Status.choices)
    template_color = IntegerField(default=1)
    is_configured = BooleanField(db_default=True)
    is_sub_domain = BooleanField(db_default=True)
    shop = OneToOneField('shops.Shop', CASCADE)


class TelegramBot(Model):
    username = CharField(max_length=255, unique=True)
    token = CharField(max_length=255, unique=True)
    group_access_token = CharField(max_length=255, unique=True)
    is_new_template = BooleanField()
    order_button_url = CharField(max_length=255)
    shop = OneToOneField('shops.Shop', CASCADE)


class Plan(CreatedBaseModel):
    code = CharField(max_length=150)
    name = CharField(max_length=150)
    description = TextField(max_length=150)


class PlanPricing(CreatedBaseModel):
    price = FloatField(default=0.0)
    original_price = FloatField(default=0.0)
    name = CharField(max_length=50)
    period = IntegerField(default=30)
    currency = OneToOneField('shops.Currency', CASCADE)
    plan = ForeignKey('shops.Plan', CASCADE)


class PlanQuotas(CreatedBaseModel):
    name = CharField(max_length=150)
    description = TextField(null=True, blank=True)
    value = CharField(max_length=50, null=True, blank=True)
    plan = ForeignKey('shops.Plan', CASCADE)
