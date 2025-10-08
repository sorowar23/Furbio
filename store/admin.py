from django.contrib import admin
from .models import Product, Variation, ProductImage,ReviewRating
# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3   # show 3 upload slots by default

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','sale_price','stock','category','modified_date','is_available', "is_featured", "is_hot_sale")
    prepopulated_fields = {'slug':('product_name',)}
    list_editable = ("sale_price","is_featured", "is_hot_sale")  # Quick toggle
    inlines = [ProductImageInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable =('is_active',)
    list_filter = ('product','variation_category','variation_value')



admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
