from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import TextChoices, Model, DateTimeField, CharField, SlugField, FloatField, ForeignKey, \
    IntegerField, CASCADE, TextField, FileField, ImageField
from django.utils.text import slugify
from django_resized import ResizedImageField


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_et = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseSlugModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class Region(Model):
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    class Role(TextChoices):
        ADMIN = "admin", 'Admin'
        OPERATOR = "operator", 'Operator'
        MANAGER = "manager", 'Manager'
        SELLER = "seller", 'Seller'
        USER = "user", 'User'

    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    role = CharField(max_length=50, choices=Role.choices, default=Role.USER)
    phone_number = CharField(db_column='user_phone_number', max_length=12, unique=True)


class Product(BaseModel, BaseSlugModel):
    price = FloatField()
    category = ForeignKey('apps.Category', on_delete=CASCADE, to_field='slug', related_name='products')
    order_count = IntegerField(default=0)
    description = TextField()
    video = FileField(upload_to='videos', null=True, blank=True,
                      validators=[
                          FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    store = ForeignKey('apps.Store', on_delete=CASCADE, related_name='products')


def __str__(self):
    return self.name


class Category(BaseSlugModel):
    image = ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class ProductImage(Model):
    image = ResizedImageField(size=[200, 200], quality=100, upload_to='products/')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='images')


class Order(BaseModel):
    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    product = ForeignKey('apps.Product', CASCADE, related_name='orders')
    phone_number = CharField(max_length=25)
    full_name = CharField(max_length=255)


class Store(BaseModel):
    name = CharField(max_length=255, default=None)
    owner = ForeignKey('apps.User', on_delete=CASCADE, related_name='store')
    image = ImageField(upload_to='static/images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    text = CharField(max_length=255, null=True, blank=True)
    user = ForeignKey(User, on_delete=CASCADE)
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='comments')

    def __str__(self):
        return self.text
