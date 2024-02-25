import os
from django.contrib import admin
from shop import models as sh_models
from shop import utils as sh_utils
from django.conf import settings

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(sh_models.Category, CategoryAdmin)


class ProductImageInline(admin.TabularInline):
    model = sh_models.ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        """
        Personnalise la sauvegarde d'une instance de Product dans l'administration Django.
        """
        super().save_model(request, obj, form, change)
        output_dir = os.path.join(settings.MEDIA_ROOT, "images")

        # Vérifie si l'instance est une nouvelle instance ou une instance modifiée
        # if not change 
        # Si c'est une nouvelle instance, traite les images associées à ce produit
        # Vérifie s'il existe des images associées à ce produit
        if obj.images.exists():
            thumbnail_path, large_path = sh_utils.process_product_images(obj.id, output_dir)
            # Vous pouvez enregistrer ces chemins dans la base de données ou les utiliser comme bon vous semble
            obj.thumbnail_path = thumbnail_path
            obj.large_path = large_path
            obj.save()


admin.site.register(sh_models.Product, ProductAdmin)
admin.site.register(sh_models.ProductImage)
#-- Attributs
admin.site.register(sh_models.ProductItem)
admin.site.register(sh_models.ProductAttribute)
admin.site.register(sh_models.ProductAttributeValue)
