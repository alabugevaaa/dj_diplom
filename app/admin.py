from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import OrderDetail, Order, Item, Category, Article, Review


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInline]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
