from django.db.models import DateTimeField, Model, SlugField
from django.utils.text import slugify


class CreatedBaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugBaseModel(Model):
    slug = SlugField(max_length=100, unique=True, editable=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(force_insert, force_update, using, update_fields)

    def generate_slug(self):
        base_slug = slugify(self.get_slug_source())
        slug = base_slug
        num = 1

        while self.__class__.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{num}'
            num += 1

        return slug

    def get_slug_source(self):
        raise NotImplementedError("Subclasses must implement get_slug_source method")

    class Meta:
        abstract = True
