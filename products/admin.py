from django.contrib import admin
from .models import Category, Product
from django.utils.translation import gettext_lazy as _


class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for managing Category model."""
    list_display = ('name', 'parent', 'slug', 'description')  # Remove 'created_at' field
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'parent', 'description')
        }),
    )

class ProductAdmin(admin.ModelAdmin):
    """Admin interface for managing Product model."""
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created', 'updated', 'rating')
    list_filter = ('category', 'available', 'created')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created',)
    date_hierarchy = 'created'
    actions = ['make_available', 'make_unavailable']

    def make_available(self, request, queryset):
        queryset.update(available=True)
        self.message_user(request, _("Selected products are now available."))

    def make_unavailable(self, request, queryset):
        queryset.update(available=False)
        self.message_user(request, _("Selected products are now unavailable."))

    make_available.short_description = _('Mark selected as available')
    make_unavailable.short_description = _('Mark selected as unavailable')

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'price', 'category', 'image', 'stock', 'rating')
        }),
        (_('Availability'), {
            'fields': ('available',),
        }),
        (_('Dates'), {
            'fields': ('created', 'updated'),
        }),
    )
    readonly_fields = ('created', 'updated')  # Make created and updated fields readonly

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
