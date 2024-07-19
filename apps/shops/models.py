from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, TextChoices, ManyToManyField, \
    IntegerField, FloatField, BooleanField, DateTimeField, OneToOneField, URLField, PositiveSmallIntegerField, \
    TimeField, DecimalField, CheckConstraint, Q, F, PositiveIntegerField

from shared.django.models import CreatedBaseModel


class Country(Model):  # ✅
    name = CharField('Nomi', max_length=100)

    class Meta:
        verbose_name = 'Davlat'
        verbose_name_plural = 'Davlatlar'


class Language(Model):  # ✅
    title = CharField('Nomi', max_length=50)
    code = CharField('Kodi', max_length=10)
    icon = CharField('Belgisi', max_length=10)


class ShopCategory(Model):  # ✅
    name = CharField('Nomi', max_length=100)

    class Meta:
        verbose_name = 'Do\'kon toifasi'
        verbose_name_plural = 'Do\'kon toifalari'

    def __str__(self):
        return self.name


class Currency(Model):  # ✅
    name = CharField('Nomi', max_length=100)
    order = PositiveSmallIntegerField('Rangi', default=1, db_default=1)

    class Meta:
        verbose_name = 'Pul birligi'
        verbose_name_plural = 'Pul birliklari'

    def __str__(self):
        return self.name


class Shop(CreatedBaseModel):  # ✅
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        IN_ACTIVE = 'inactive', 'Inactive'

    name = CharField("Do'kon nomi", max_length=255)
    phone = CharField("Biznes telefon raqami", max_length=50)
    phone_number = CharField("Telefon raqami", max_length=50)

    country = ForeignKey("shops.Country", CASCADE, verbose_name="Ro'yxatdan o'tgan davlat")
    languages = ManyToManyField("shops.Language", blank=True, verbose_name="Til")
    services = ManyToManyField('orders.Service', through='orders.ShopService')
    category = ForeignKey("shops.ShopCategory", CASCADE, verbose_name="Kategoriyalar")
    status = CharField(max_length=8, choices=Status.choices, db_default=Status.ACTIVE)
    currency = ForeignKey("shops.Currency", CASCADE, verbose_name="Pul birligi")
    plan = ForeignKey('users.Plan', CASCADE, related_name='shops')
    owner = ForeignKey('users.User', CASCADE, related_name='shops')
    lat = FloatField('Location lat', blank=True, null=True)
    lon = FloatField('Location lon', blank=True, null=True)
    starts_at = TimeField('Dan', blank=True, null=True)
    ends_at = TimeField('Gacha', blank=True, null=True)
    has_terminal = BooleanField(db_default=True)
    about_us = TextField("Biz haqimizda", null=True, blank=True)
    facebook = URLField("Facebook", max_length=255, null=True, blank=True)
    instagram = URLField("Instagram", max_length=255, null=True, blank=True)
    telegram = URLField('Telegram', max_length=255, null=True, blank=True)
    email = URLField("Elektron pochta", max_length=255, null=True, blank=True)
    address = CharField('Manzil', max_length=500, null=True, blank=True)
    is_new_products_show = BooleanField("'Yangi mahsulotlar' sahifasini ko'rsatish", default=False, db_default=False)
    is_popular_products_show = BooleanField("'Ommabop mahsulotlar' sahifasini ko'rsatish", default=False,
                                            db_default=False)
    attachments = GenericRelation('shops.Attachment', blank=True)
    shop_logo = GenericRelation('shops.Attachment', blank=True)
    favicon_image = GenericRelation('shops.Attachment', blank=True)
    slider_images = GenericRelation('shops.Attachment', blank=True)


class TemplateColor(Model):  # ✅
    name = CharField('Nomi', max_length=55)
    color = CharField('Rangi', max_length=55)

    class Meta:
        verbose_name = 'Shablon rangi'
        verbose_name_plural = 'Shablon ranglari'

    def __str__(self):
        return self.name


class TelegramChannel(Model):  # ✅
    chat = CharField('Telegram kanal username', max_length=255)
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
    is_scheduled = BooleanField("Keyinroq jo'natilsinmi?", default=False)
    scheduled_time = DateTimeField("Keyinroq jo'natish vaqti", blank=True, null=True)
    file_type = CharField(max_length=20, choices=FileType.choices, db_default=FileType.TEXT)
    status = CharField('Xabarning statusi', max_length=20, choices=MessageStatus.choices,
                       db_default=MessageStatus.PENDING)
    created_at = DateTimeField('Xabar yaratilgan vaqti', auto_now_add=True)

    class Meta:
        verbose_name = 'Telegram kanal xabari'
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
    content_type = CharField(max_length=10, choices=Type.choices)
    seen = BooleanField(db_default=False)
    created_at = DateTimeField('Yaratilgan vaqti', auto_now_add=True)


class BroadCastMessage(Model):  # ✅
    class MessageStatus(TextChoices):
        SENT = 'sent', 'Sent'
        PENDING = 'pending', 'Pending'
        NOT_SENT = 'not_sent', 'Not sent'

    message = CharField('Xabar', max_length=4100)
    shop = ForeignKey('shops.Shop', CASCADE)
    is_scheduled = BooleanField(default=False)
    lat = FloatField("Lokatsiya lat", blank=True, null=True)
    lon = FloatField("Lokatsiya lon", blank=True, null=True)
    scheduled_time = DateTimeField("Keyinroq jo'natish vaqti", blank=True, null=True)
    received_users = IntegerField('Qabul qiluvchilar soni', default=0)
    status = CharField('Xabarning statusi', max_length=20, choices=MessageStatus.choices,
                       db_default=MessageStatus.PENDING)
    attachments = GenericRelation('shops.Attachment', blank=True)
    created_at = DateTimeField('Yaratilgan sana', auto_now_add=True)

    class Meta:
        verbose_name = 'Axborotnoma'
        verbose_name_plural = 'Axborotnomalar'


class Commerce(Model):  # ✅
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    name = CharField('Domen Nomi', max_length=30)
    status = CharField('Sayt aktiv yoki  aktivmasligi', max_length=8, choices=Status.choices)
    template_color = ForeignKey('shops.TemplateColor', CASCADE, related_name='sites')
    is_configured = BooleanField(db_default=True)
    is_sub_domain = BooleanField('Sayt domen qo`ygan yoki qo`ymaganligi', db_default=True)
    shop = OneToOneField('shops.Shop', CASCADE, related_name='sites')


class TelegramBot(Model):  # ✅
    username = CharField("Telegram username", max_length=255, unique=True)
    token = CharField('BotFather dan olingan token', max_length=255, unique=True)
    group_access_token = CharField('guruhda ishlashi uchun token', max_length=255, unique=True)
    is_new_template = BooleanField('web app True oddiy bot False')
    order_button_url = CharField(max_length=255)
    shop = OneToOneField('shops.Shop', CASCADE, related_name='telegram_bots')


class Category(Model):  # ✅
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    name = CharField('Nomi', max_length=255)
    emoji = CharField('Emoji', max_length=25, null=True, blank=True)
    parent = ForeignKey('self', CASCADE, blank=True, null=True, related_name='children')
    show_in_ecommerce = BooleanField("Web saytda ko'rsatish", db_default=False)
    status = CharField('Holati', max_length=15, choices=Status.choices, db_default=Status.INACTIVE)
    description = TextField('Tavsif', null=True, blank=True)
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

    name = CharField('Mahsulot nomi', max_length=100)
    category = ForeignKey('shops.Category', CASCADE, related_name='products')
    price = DecimalField('Sotuv narxi', max_digits=15, decimal_places=2)
    full_price = DecimalField('Umumiy narxi', max_digits=15, decimal_places=2)
    description = TextField()
    has_available = BooleanField('Mahsulotni o`chirish va yoqish', default=True)
    weight = IntegerField('Vazni', null=True, blank=True)
    length = IntegerField("Uzunligi", null=True, blank=True)
    height = IntegerField('Balandligi', null=True, blank=True)
    width = IntegerField("Kengligi", null=True, blank=True)

    ikpu_code = IntegerField('IKPU ko`di', null=True, blank=True)
    package_code = IntegerField('qadoq ko`di', null=True, blank=True)
    stock_status = CharField(max_length=100, choices=StockStatus.choices)
    quantity = IntegerField('mahsulot soni status indefinite bo`lganda chiqadi', db_default=0)
    barcode = IntegerField('Barkod', null=True, blank=True)
    vat_percent = IntegerField('QQS foizi', db_default=0)
    position = IntegerField('sort order', db_default=1)
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
    weight = IntegerField('Vazni', null=True, blank=True)
    length = IntegerField('Uzunligi', null=True, blank=True)
    height = IntegerField('Balandligi', null=True, blank=True)
    width = IntegerField("Kengligi", null=True, blank=True)
    package_code = IntegerField('', null=True, blank=True)
    ikpu_code = IntegerField('IKPU kodi', null=True, blank=True)
    stock_status = CharField('Miqdorlar statusi', max_length=20)
    quantity = IntegerField('Miqdori', null=True, blank=True)
    unit = CharField('Qadoq kodi', max_length=20)
    barcode = IntegerField('Shtrix-kod', null=True, blank=True)
    has_available = BooleanField('Mavjud yoki mavjudmasligi', db_default=True)
    vat_percent = IntegerField('QQS foizi', db_default=0)
    product = ForeignKey('shops.Product', CASCADE, related_name='variants')
