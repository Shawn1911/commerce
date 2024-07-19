from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, TextChoices, IntegerField, BooleanField, \
    JSONField, DateTimeField, PositiveIntegerField, ManyToManyField, SET_NULL, FloatField, DecimalField, RESTRICT

from shared.django.models import CreatedBaseModel


class Order(Model):  # ✅
    class Status(TextChoices):
        IN_PROCESSING = 'in_processing', 'In Process'
        CANCELLED = 'cancelled', 'Cancelled'
        CONFIRMED = 'confirmed', 'Confirmed'
        PERFORMING = 'performing', 'Performing'
        PERFORMED = 'performed', 'Performed'
        REFUNDED = 'refunded', 'Refunded'

    class Type(TextChoices):
        TELEGRAM = 'telegram', 'Telegram'
        WEB = 'web', 'Web'

    class DeliveryType(TextChoices):
        ONLINE_DELIVERY = 'online_delivery', 'Online Delivery'
        DELIVERY = 'delivery', 'Delivery'
        PICKUP = 'pickup', 'Pickup'

    delivery_price = DecimalField('Yetkazib berish narxi', null=True, blank=True, decimal_places=2, max_digits=15)
    # user = ForeignKey('users.ShopUser', SET_NULL, null=True, blank=True, verbose_name='Teligram chat id')
    payment = ForeignKey('orders.ShopService', SET_NULL, null=True, blank=True, related_name='orders')
    status = CharField('Order Statusi', max_length=20, choices=Status.choices)
    paid = BooleanField("To'lov qilingan yoki yo'qligi", db_default=False)

    promo_code = ForeignKey('orders.PromoCode', SET_NULL, null=True, blank=True, related_name='orders')
    note = TextField('Description', null=True, blank=True)
    delivery_date = DateTimeField('Yetkazib berish vaqti', null=True, blank=True)
    delivery_type = CharField(max_length=50, choices=DeliveryType.choices)
    order_type = CharField(max_length=20, choices=Type.choices)

    is_archived = BooleanField('Arxivlangan buyurtmalar', db_default=False)
    yandex_taxi_link = CharField(max_length=255, null=True, blank=True)
    currency = ForeignKey('shops.Currency', RESTRICT, related_name='orders')
    address = CharField('Manzil', max_length=255, null=True, blank=True)
    lon = FloatField(null=True, blank=True)
    lat = FloatField(null=True, blank=True)
    entrance = CharField('Kirish joyi', max_length=50, null=True, blank=True)
    door_phone = CharField('eshik telfon raqami', max_length=50, null=True, blank=True)
    floor_number = IntegerField('Qavat raqami', null=True, blank=True)
    apartment_number = IntegerField('kvartera raqami', null=True, blank=True)

    first_name = CharField('Haridorni ismi', max_length=50)  # register qilgan paytdagi ismni oladi
    last_name = CharField('Haridorni familiyasi', max_length=50)  # register qilgan paytdagi familiyani oladi
    phone = CharField('Haridorni telfon raqami ', max_length=50)  # kiritsh majburiy
    created_at = DateTimeField('Buyurtma yaratilgan vaqti', auto_now_add=True)


class OrderItem(Model):  # ✅
    order = ForeignKey('orders.Order', CASCADE, related_name='items')
    count = PositiveIntegerField('Soni', db_default=1)
    currency = ForeignKey('shops.Currency', RESTRICT)
    product_attribute = ForeignKey('shops.AttributeVariant', CASCADE, related_name='order_items')


class PromoCode(CreatedBaseModel):  # ✅
    class Type(TextChoices):
        FREE_DELIVERY = 'free_delivery', 'Free delivery'
        DISCOUNT = 'discount', 'Discount'

    active = BooleanField('Faolligi', default=True)
    code = CharField('Promokod', max_length=255)
    start_date = DateTimeField(verbose_name='Amal qilish muddati(boshi)')
    end_date = DateTimeField(verbose_name='Amal qilish muddati(oxiri)')
    limit = IntegerField(verbose_name='Soni')
    remaining_quantity = IntegerField(verbose_name='Qolgan miqdor')
    type = CharField('Tur', max_length=255, choices=Type.choices, default=Type.FREE_DELIVERY)
    percent = IntegerField(db_default=0)
    used_quantity = PositiveIntegerField()
    shop = ForeignKey('shops.Shop', CASCADE, related_name='promo_codes')

    class Meta:
        verbose_name = 'Promo kod'
        verbose_name_plural = 'Promo kodlar'
        unique_together = [
            ('code', 'shop')
        ]


class ShopService(Model):  # ✅
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        NOT_EXISTS = 'not_exists', 'Not exists'

    shop = ForeignKey('shops.Shop', CASCADE)
    service = ForeignKey('orders.Service', CASCADE)
    status = CharField(max_length=15, choices=Status.choices, db_default=Status.INACTIVE)
    fields = ManyToManyField('orders.Field', through='orders.ShopServiceField')


class Service(Model):  # ✅
    class ServiceType(TextChoices):
        DELIVERY = 'delivery', 'Delivery'
        PAYMENT = 'payment', 'Payment'

    class Type(TextChoices):
        INTERNAL = 'internal', 'Internal'
        INPLACE = 'inplace', 'Inplace'
        TELEGRAM = 'telegram', 'Telegram'
        WEB = 'web', 'Web'
        INSTALMENT = 'instalment', 'Instalment'

    service_type = CharField(max_length=15, choices=ServiceType.choices)
    title = CharField('Sarlavha', max_length=255)
    code = CharField(max_length=255)
    type = CharField(max_length=255, choices=Type.choices)
    description = TextField('tavsifi',null=True, blank=True)
    attachments = GenericRelation('shops.Attachment', blank=True)

    class Meta:
        unique_together = [
            ('code', 'type')
        ]


class ShopServiceField(Model):  # ✅
    shop_service = ForeignKey('orders.ShopService', CASCADE)
    field = ForeignKey('orders.Field', CASCADE)
    value = JSONField(default=dict)


class Field(Model):  # ✅
    class Type(TextChoices):
        INTEGER = 'integer', 'Integer'
        STRING = 'string', 'String'
        TEXT = 'text', 'Text'
        LIST = 'list', 'List'
        VIDEO = 'video', 'Video'
        IMAGE = 'image', 'Image'
        GEOLOCATION = 'geolocation', 'Geolocation'

    service = ForeignKey('orders.Service', CASCADE, related_name='fields')
    label = CharField(max_length=255)
    name = CharField(max_length=255, unique=True)
    max_length = IntegerField()
    required = BooleanField()
    type = CharField(max_length=255, choices=Type.choices)
    provider_labels = JSONField(null=True, blank=True)
