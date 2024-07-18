from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, TextChoices, ManyToManyField, \
    IntegerField, FloatField, BooleanField, DateTimeField, OneToOneField, URLField, PositiveSmallIntegerField, \
    TimeField, DecimalField, CheckConstraint, Q, F, PositiveIntegerField

from shared.django.models import CreatedBaseModel


class Country(Model):  # ✅
    name = CharField(max_length=100, verbose_name='Nomi')

    class Meta:
        verbose_name = 'Davlat'
        verbose_name_plural = 'Davlatlar'


class Language(Model):  # ✅
    title = CharField(max_length=50, verbose_name='Nomi')
    code = CharField(max_length=10, verbose_name='Kodi')
    icon = CharField(max_length=10, verbose_name='Belgisi')


class ShopCategory(Model):  # ✅
    name = CharField(max_length=100, verbose_name='Nomi')

    class Meta:
        verbose_name = 'Do\'kon toifasi'
        verbose_name_plural = 'Do\'kon toifalari'

    def __str__(self):
        return self.name


class Currency(Model):  # ✅
    name = CharField(max_length=100, verbose_name='Nomi')
    order = PositiveSmallIntegerField(default=1, db_default=1, verbose_name='Rangi')

    class Meta:
        verbose_name = 'Pul birligi'
        verbose_name_plural = 'Pul birliklari'

    def __str__(self):
        return self.name


class Shop(CreatedBaseModel):  # ✅
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        IN_ACTIVE = 'inactive', 'Inactive'

    name = CharField(max_length=255, verbose_name="Do'kon nomi")
    phone = CharField(max_length=50, verbose_name="Biznes telefon raqami")
    phone_number = CharField(max_length=50, verbose_name="Telefon raqami")

    country = ForeignKey("shops.Country", CASCADE, verbose_name="Ro'yxatdan o'tgan davlat")
    languages = ManyToManyField("shops.Language", blank=True, verbose_name="Til")
    services = ManyToManyField('orders.Service', through='orders.ShopService')
    category = ForeignKey("shops.ShopCategory", CASCADE, verbose_name="Kategoriyalar")
    status = CharField(max_length=8, choices=Status.choices, db_default=Status.ACTIVE)
    currency = ForeignKey("shops.Currency", CASCADE, verbose_name="Pul birligi")
    plan = ForeignKey('users.Plan', CASCADE, related_name='shops')
    owner = ForeignKey('users.User', CASCADE, related_name='shops')
    lat = FloatField(blank=True, null=True)
    lon = FloatField(blank=True, null=True)
    starts_at = TimeField(blank=True, null=True, verbose_name="Dan")
    ends_at = TimeField(blank=True, null=True, verbose_name="Gacha")
    has_terminal = BooleanField(db_default=True)
    about_us = TextField(null=True, blank=True, verbose_name="Biz haqimizda")
    facebook = URLField(max_length=255, null=True, blank=True, verbose_name="Facebook")
    instagram = URLField(max_length=255, null=True, blank=True, verbose_name="Instagram")
    telegram = URLField('Telegram', max_length=255, null=True, blank=True)
    email = URLField(max_length=255, null=True, blank=True, verbose_name="Elektron pochta")
    address = CharField('Manzil', max_length=500, null=True, blank=True)
    is_new_products_show = BooleanField(default=False, db_default=False,
                                        verbose_name="'Yangi mahsulotlar' sahifasini ko'rsatish")
    is_popular_products_show = BooleanField(default=False, db_default=False,
                                            verbose_name="'Ommabop mahsulotlar' sahifasini ko'rsatish")


class TemplateColor(Model):  # ✅
    name = CharField(max_length=55, verbose_name='Nomi')
    color = CharField(max_length=55, verbose_name='Rangi')

    class Meta:
        verbose_name = 'Shablon rangi'
        verbose_name_plural = 'Shablon ranglari'

    def __str__(self):
        return self.name


class TelegramChannel(Model):  # ✅
    chat = CharField(max_length=255, verbose_name='Telegram kanal username')
    shop = ForeignKey('shops.Shop', CASCADE, related_name='channels')

    class Meta:
        verbose_name = 'Telegram kanal'
        verbose_name_plural = 'Telegram kanallar'
        unique_together = [
            ('shop', 'chat')
        ]

    def __str__(self):
        return f"{self.chat}"


class ChannelMessage(Model):  # ✅
    class FileType(TextChoices):
        TEXT = 'text', 'Text'
        PHOTO = 'photo', 'Photo'
        VIDEO = 'video', 'Video'

    class MessageStatus(TextChoices):
        SENT = 'sent', 'Sent'
        PENDING = 'pending', 'Pending'
        NOT_SENT = 'not_sent', 'Not sent'

    message = CharField(max_length=4100)
    chat = ForeignKey('shops.TelegramChannel', CASCADE, related_name='messages')
    is_scheduled = BooleanField(default=False)
    scheduled_time = DateTimeField(blank=True, null=True, verbose_name="Keyinroq jo'natish vaqti")
    file_type = CharField(max_length=20, choices=FileType.choices, db_default=FileType.TEXT)
    status = CharField('Xabarning statusi', max_length=20, choices=MessageStatus.choices,
                       db_default=MessageStatus.PENDING)
    created_at = DateTimeField(auto_now_add=True, verbose_name='Xabar yaratilgan vaqti')

    class Meta:
        verbose_name = 'Telegram Kanal xabari'
        verbose_name_plural = 'Telegram kanal xabarlari'

    def __str__(self):
        return f"{self.id}. Message of {self.chat}"


class ChatMessage(Model):  # ✅
    class Type(TextChoices):
        USER = 'user', 'User'
        OWNER = 'owner', 'Owner'

    class ContentType(TextChoices):
        TEXT = 'text', 'Text'

    message = CharField('Xabar', max_length=4100)
    # chat_user = ForeignKey('users.ShopUser', CASCADE, related_name='messages')
    content_type = CharField(max_length=10, choices=Type.choices)
    seen = BooleanField(db_default=False)
    created_at = DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')


class BroadCastMessage(Model):  # ✅
    class MessageStatus(TextChoices):
        SENT = 'sent', 'Sent'
        PENDING = 'pending', 'Pending'
        NOT_SENT = 'not_sent', 'Not sent'

    message = CharField(max_length=4100, verbose_name='Xabar')
    shop = ForeignKey('shops.Shop', CASCADE)
    is_scheduled = BooleanField(default=False)
    lat = FloatField(blank=True, null=True, verbose_name="Lokatsiya lat")
    lon = FloatField(blank=True, null=True, verbose_name="Lokatsiya lon")
    scheduled_time = DateTimeField(blank=True, null=True, verbose_name="Keyinroq jo'natish vaqti")
    received_users = IntegerField(default=0, verbose_name='Qabul qiluvchilar soni')
    status = CharField('Xabarning statusi', max_length=20, choices=MessageStatus.choices,
                       db_default=MessageStatus.PENDING)
    created_at = DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')

    class Meta:
        verbose_name = 'Axborotnoma'
        verbose_name_plural = 'Axborotnomalar'


class Commerce(Model):  # ✅
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    name = CharField(max_length=30, verbose_name='Domen Nomi')
    status = CharField(max_length=8, choices=Status.choices, verbose_name='Sayt aktiv yoki  aktivmasligi')
    template_color = ForeignKey('shops.TemplateColor', CASCADE, related_name='sites')
    is_configured = BooleanField(db_default=True)
    is_sub_domain = BooleanField(db_default=True, verbose_name='Sayt domen quygan yoki yuqligi')
    shop = OneToOneField('shops.Shop', CASCADE, related_name='sites')


class TelegramBot(Model):  # ✅
    username = CharField(max_length=255, unique=True, verbose_name='Telegram username')
    token = CharField(max_length=255, unique=True, verbose_name='BotFather dan olingan token')
    group_access_token = CharField(max_length=255, unique=True, verbose_name='guruhda ishlashi uchun token')
    is_new_template = BooleanField(verbose_name='web app True odiiy bot False')
    order_button_url = CharField(max_length=255)
    shop = OneToOneField('shops.Shop', CASCADE, related_name='telegram_bots')


class Category(Model):  # ✅
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    name = CharField(max_length=255)
    emoji = CharField(max_length=25, null=True, blank=True)
    parent = ForeignKey('self', CASCADE, blank=True, null=True, related_name='children')
    show_in_ecommerce = BooleanField(db_default=False)
    status = CharField(max_length=15, choices=Status.choices, db_default=Status.INACTIVE)
    description = TextField(null=True, blank=True)
    position = IntegerField(default=1)
    shop = ForeignKey('shops.Shop', CASCADE, related_name='categories')
    attachments = GenericRelation('shops.Attachment', blank=True)

class Weight(Model):  # ✅
    name = CharField(max_length=10)


class Length(Model):  # ✅
    name = CharField(max_length=10)


class Product(Model):  # ✅
    class StockStatus(TextChoices):
        FIXED = 'fixed', 'Fixed'
        INDEFINITE = 'indefinite', 'Indefinite'
        NOT_AVAILABLE = 'not_available', 'Not available'

    class Unit(TextChoices):
        ITEM = 'item', 'Item'
        WEIGHT = 'weight', 'Weight'

    name = CharField('Product nomi', max_length=100)
    category = ForeignKey('shops.Category', CASCADE, related_name='products')
    price = DecimalField('Sotuv narxi', max_digits=15, decimal_places=2)
    full_price = DecimalField('Umumiy narxi', max_digits=15, decimal_places=2)
    description = TextField()
    has_available = BooleanField(default=True, verbose_name='MAxsulotni uchirish va yoqish')
    weight = IntegerField(null=True, blank=True)
    length = IntegerField(null=True, blank=True)
    height = IntegerField(null=True, blank=True)
    width = IntegerField(null=True, blank=True)

    ikpu_code = IntegerField(null=True, blank=True, verbose_name='IKPU kod')
    package_code = IntegerField(null=True, blank=True, verbose_name='qadoq kodi')
    stock_status = CharField(max_length=100, choices=StockStatus.choices)
    quantity = IntegerField(db_default=0, verbose_name='product soni status indefinite bulganda chiqadi')
    barcode = IntegerField(null=True, blank=True, verbose_name='Barkod')
    vat_percent = IntegerField(db_default=0, verbose_name='QQS foizi')
    position = IntegerField(db_default=1, verbose_name='sort order')
    internal_notes = TextField(null=True, blank=True)
    unit = CharField(max_length=20, choices=Unit.choices)
    weight_class = ForeignKey('shops.Weight', CASCADE, related_name='weights')
    length_class = ForeignKey('shops.Length', CASCADE, related_name='lengths')
    attachments = GenericRelation('shops.Attachment', blank=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(full_price__gte=F('price')), name='check_full_price')
        ]


class Attachment(CreatedBaseModel):
    content_type = ForeignKey('contenttypes.ContentType', CASCADE, null=True, blank=True, related_name='attachments')
    record_id = PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'record_id')
    key = CharField(max_length=255, null=True, blank=True)
    url = URLField(null=True, blank=True)


class Attribute(Model):  # ✅
    name = CharField(max_length=50)
    product = ForeignKey('shops.Product', CASCADE, related_name='attributes')


class AttributeValue(Model):  # ✅
    value = CharField(max_length=20)
    attribute = ForeignKey('shops.Attribute', CASCADE, related_name='values')


class AttributeVariant(Model):  # ✅
    name = CharField(max_length=100)
    price = DecimalField('Sotuv narxi', max_digits=15, decimal_places=2)
    full_price = DecimalField('Umumiy narxi', max_digits=15, decimal_places=2)
    weight_class = ForeignKey('shops.Weight', CASCADE, null=True, blank=True, related_name='attribute_weights')
    length_class_id = ForeignKey('shops.Length', CASCADE, null=True, blank=True, related_name='attribute_lengths')
    weight = IntegerField(null=True, blank=True)
    length = IntegerField(null=True, blank=True)
    height = IntegerField(null=True, blank=True)
    width = IntegerField(null=True, blank=True)
    package_code = IntegerField(null=True, blank=True)
    ikpu_code = IntegerField(null=True, blank=True)
    stock_status = CharField(max_length=20)
    quantity = IntegerField(null=True, blank=True)
    unit = CharField(max_length=20)
    barcode = IntegerField(null=True, blank=True)
    has_available = BooleanField(db_default=False)
    vat_percent = IntegerField(db_default=0)
    product = ForeignKey('shops.Product', CASCADE, related_name='variants')
