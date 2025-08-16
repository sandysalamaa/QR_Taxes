from django.contrib import admin

from core.models import Category,Item,Receipt

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "created_at")
    list_editable = ("sort_order",)  
    ordering = ("sort_order",)
    

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('merchant_name', 'user', 'total_price', 'scan_date')
    list_filter = ('scan_date', 'user')
    raw_id_fields = ('user',)
    date_hierarchy = 'scan_date'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'invoice', 'category', 'quantity', 'unit_price', 'total_price')
    list_filter = ('category',)
    search_fields = ('name', 'invoice__merchant_name')