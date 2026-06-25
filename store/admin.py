from django.contrib import admin
from .models import Category,Product,Order


@admin.register(Category)
class CategoryDetail(admin.ModelAdmin):
    list_display = ["id","name"]

@admin.register(Product)
class ProductDetails(admin.ModelAdmin):
    list_display = ["name","price","category","stock"]
    list_filter = ["category","price"]
    ordering = ["id"]
@admin.register(Order)
class OrderDetail(admin.ModelAdmin):
    list_display = ["id","customer_name","product","quantity"]
    ordering = ["id"]



