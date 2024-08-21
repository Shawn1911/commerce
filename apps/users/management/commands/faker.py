import random

from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from orders.models import Service
from shops.models import (Category, Country, Currency, Language, Length,
                          Product, Shop, ShopCategory, Weight,)
from users.models import Plan, User


class Command(BaseCommand):
    help = 'Generates N fake records for specified model (user, shop, category, product)'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str,
                            help='The model to populate with fake data: user, shop, category, product')
        parser.add_argument('n', type=int, help='The number of fake records to create')

    def handle(self, *args, **kwargs):
        model = kwargs['model'].lower()
        n = kwargs['n']

        fake = Faker()

        if model == 'user':
            self.create_fake_users(n, fake)
        elif model == 'shop':
            self.create_fake_shops(n, fake)
        elif model == 'category':
            self.create_fake_categories(n, fake)
        elif model == 'product':
            self.create_fake_products(n, fake)
        else:
            raise CommandError('Invalid model. Please specify one of the following: user, shop, category, product.')

    def create_fake_users(self, n, fake):
        available_languages = list(Language.objects.all())
        available_shops = list(Shop.objects.all())

        for _ in range(n):
            type_choice = random.choice(User.Type.values)
            username = fake.unique.user_name()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            invitation_code = fake.unique.lexify(text='????????',
                                                 letters='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')

            language = random.choice(available_languages) if available_languages else None
            default_shop = random.choice(available_shops) if available_shops else None

            user = User.objects.create(
                type=type_choice,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_staff=fake.boolean(),
                is_active=fake.boolean(),
                language=language,
                public_offer=fake.boolean(),
                invitation_code=invitation_code,
                default_shop=default_shop,
            )
            user.set_password('password123')
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Created User: {user.username}'))

    def create_fake_shops(self, n, fake):
        available_countries = list(Country.objects.all())
        available_languages = list(Language.objects.all())
        available_services = list(Service.objects.all())
        available_categories = list(ShopCategory.objects.all())
        available_currencies = list(Currency.objects.all())
        available_plans = list(Plan.objects.all())
        available_users = list(User.objects.all())

        if not all([available_countries, available_categories, available_currencies, available_plans, available_users]):
            raise CommandError('Ensure there are countries, categories, currencies, plans, and users available.')

        for _ in range(n):
            country = random.choice(available_countries)
            category = random.choice(available_categories)
            currency = random.choice(available_currencies)
            plan = random.choice(available_plans)
            owner = random.choice(available_users)

            shop = Shop.objects.create(
                name=fake.company(),
                phone=fake.phone_number(),
                phone_number=fake.phone_number(),
                country=country,
                category=category,
                status=random.choice(Shop.Status.values),
                currency=currency,
                plan=plan,
                owner=owner,
                lat=fake.latitude(),
                lon=fake.longitude(),
                starts_at=fake.time_object(),
                ends_at=fake.time_object(),
                has_terminal=fake.boolean(),
                about_us=fake.paragraph(nb_sentences=3),
                facebook=fake.url(),
                instagram=fake.url(),
                telegram=fake.url(),
                email=fake.email(),
                address=fake.address(),
                is_new_products_show=fake.boolean(),
                is_popular_products_show=fake.boolean(),
            )

            shop.languages.set(random.sample(available_languages, k=random.randint(1, len(available_languages))))
            shop.services.set(random.sample(available_services, k=random.randint(1, len(available_services))))

            self.stdout.write(self.style.SUCCESS(f'Created Shop: {shop.name}'))

    def create_fake_categories(self, n, fake):
        # Ensure you have existing data for Shops
        available_shops = list(Shop.objects.all())

        if not available_shops:
            raise CommandError('No shops found. Please create some shops first.')

        available_categories = list(Category.objects.all())  # For potential parent categories

        for _ in range(n):
            # Randomly select a shop for each category
            shop = random.choice(available_shops)

            # Randomly select a parent category (or None)
            parent = random.choice(available_categories) if available_categories else None

            # Create a new category
            category = Category.objects.create(
                name=fake.word().capitalize(),
                emoji=fake.emoji() if random.choice([True, False]) else None,  # Randomly add an emoji
                parent=parent,
                show_in_ecommerce=fake.boolean(),
                status=random.choice(Category.Status.values),
                description=fake.paragraph(nb_sentences=3) if random.choice([True, False]) else None,
                position=random.randint(1, 100),  # Random position
                shop=shop,
            )

            self.stdout.write(self.style.SUCCESS(f'Created Category: {category.name}'))

    def create_fake_products(self, n, fake):
        # Ensure you have existing data for Categories, Weight, and Length
        categories = list(Category.objects.all())
        available_weights = list(Weight.objects.all())
        available_lengths = list(Length.objects.all())

        if not categories:
            raise CommandError('No categories found. Please create some categories first.')

        for _ in range(n):
            category = random.choice(categories)

            price = round(random.uniform(10.0, 1000.0), 2)
            full_price = round(random.uniform(price, 1500.0), 2)

            stock_status = random.choice(Product.StockStatus.values)
            unit = random.choice(Product.Unit.values)

            vat_percent = random.randint(0, 20)  # Assume VAT percent ranges from 0 to 20

            weight = random.randint(1, 100) if random.choice([True, False]) else None
            length = random.randint(1, 100) if random.choice([True, False]) else None
            height = random.randint(1, 100) if random.choice([True, False]) else None
            width = random.randint(1, 100) if random.choice([True, False]) else None

            quantity = random.randint(0, 1000) if stock_status == Product.StockStatus.INDEFINITE else 0

            # Create a new product
            product = Product.objects.create(
                name=fake.word().capitalize(),
                category=category,
                price=price,
                full_price=full_price,
                description=fake.paragraph(nb_sentences=5),
                has_available=fake.boolean(),
                weight=weight,
                length=length,
                height=height,
                width=width,
                stock_status=stock_status,
                quantity=quantity,
                vat_percent=vat_percent,
                position=random.randint(1, 100),
                internal_notes=fake.paragraph(nb_sentences=3) if random.choice([True, False]) else None,
                unit=unit
            )

            self.stdout.write(self.style.SUCCESS(f'Created Product: {product.name}'))
