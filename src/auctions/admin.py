from django.contrib import admin
from .models import Item, ItemImage



class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 0
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'created_at', 'starting_price']
    inlines = [ItemImageInline]
    search_fields = ['owner', 'title']
