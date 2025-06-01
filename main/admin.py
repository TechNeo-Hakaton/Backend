from django.contrib import admin
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, TabularInline
from .models import (
    Location, Price, Media,
    Building, Flat, Material
)

class FlatInline(TabularInline):
    model = Flat
    extra = 1


@admin.register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ('region', 'city', 'street')
    search_fields = ('region', 'city', 'street')
    ordering = ('region', 'city')


@admin.register(Price)
class PriceAdmin(ModelAdmin):
    list_display = ('rooms', 'price')
    ordering = ('rooms',)
    list_filter = ('rooms',)
    search_fields = ('rooms',)


@admin.register(Media)
class MediaAdmin(ModelAdmin):
    list_display = ('id', 'image', 'video', 'description')
    readonly_fields = ('image', 'video')
    ordering = ('-id',)


@admin.register(Building)
class BuildingAdmin(ModelAdmin):
    list_display = (
        'name', 'location', 'budget', 'flats_count',
        'start', 'end', 'status_badge', 'image_tag'
    )
    list_filter = ('status', 'start', 'end')
    search_fields = ('name', 'description')
    ordering = ('-start',)

    inlines = [FlatInline]

    def flats_count(self, obj):
        return obj.flats.count()

    flats_count.short_description = "Kvartiralar soni"
    flats_count.admin_order_field = 'flats__id'  # saralash uchun (optional)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="75" style="object-fit: cover; border-radius: 20px" />')
        return "Rasm mavjud emas"

    image_tag.short_description = "Rasm"

    def status_badge(self, obj):
        badge_colors = {
            'pending': '#6c757d',       # Gray
            'in_progress': '#fd7e14',   # Orange
            'completed': '#28a745',     # Green
            'canceled': '#dc3545',      # Red
        }
        color = badge_colors.get(obj.status, '#007bff')  # Default blue
        return mark_safe(
            f'<span style="background-color: {color}; color: white; '
            f'padding: 5px 10px; border-radius: 12px; font-size: 12px;">'
            f'{obj.get_status_display()}</span>'
        )
    status_badge.short_description = "Holat (rangli)"


@admin.register(Flat)
class FlatAdmin(ModelAdmin):
    list_display = (
        'project', 'floor', 'rooms',
        'price', 'area',
        'status', 'has_balcony', 'orientation'
    )
    list_filter = ('project', 'floor', 'rooms', 'status', 'orientation', 'has_balcony')
    search_fields = ('project__name',)
    ordering = ('project', 'floor', 'rooms')


@admin.register(Material)
class MaterialAdmin(ModelAdmin):
    list_display = (
        'name', 'unit', 'count', 'total_count',
        'company', 'building'
    )
    search_fields = ('name', 'company')
    list_filter = ('building__name', 'name', 'company')
    ordering = ('name',)
