import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey


class AbstractUUID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(AbstractUser):
    pass


@receiver(post_save, sender=User)
def send_email(sender, instance, **kwargs):
    subject = 'Регистрауия прошла успешно'
    message = f'Спасибо за регистрацию на нашем сайте.\nВаш логин: {instance.username}\nПароль: {instance._password}'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [instance.username],
        fail_silently=False,
    )


class Category(MPTTModel):
    parent = TreeForeignKey("self", blank=True, null=True, db_index=True, on_delete=models.PROTECT,
                            related_name="categories", verbose_name="Родительская категория")
    title = models.CharField(max_length=50, verbose_name="Заголовок")
    alias = models.CharField(max_length=128, blank=True, verbose_name="Ссылка")

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.title


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")
    name = models.CharField(max_length=100, verbose_name="Наименование")
    image = models.ImageField(max_length=250, upload_to='img', verbose_name="Фото")
    description = models.TextField(verbose_name="Описание товара")
    slug = models.SlugField(max_length=50, verbose_name="Метка")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name="Пользователь")
    name = models.CharField(max_length=50, verbose_name="Имя")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(max_length=250, verbose_name="Содержание")
    points = models.IntegerField(default=0, verbose_name="Оценка")
    date_add = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления отзыва")

    class Meta:
        verbose_name = 'Отыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-date_add']

    def __str__(self):
        return f'{self.user} - {self.item} - {str(self.points)}'


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    text = RichTextUploadingField(verbose_name="Текст")
    date_add = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания статьи")
    items = models.ManyToManyField(Item, related_name='articles')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-date_add']

    def __str__(self):
        return f'{self.date_add} - {self.title}'


class Order(AbstractUUID):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    items = models.ManyToManyField(Item, through="OrderDetail")

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.user} - {self.date_created} - {self.id}'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ", related_name="details")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Товар", related_name="details")
    count = models.IntegerField(default=1, verbose_name="Количество")
