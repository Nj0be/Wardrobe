from django.contrib import admin

from .models import *

admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(ProductColorImage)
admin.site.register(ProductCategory)
admin.site.register(ProductVariant)
admin.site.register(Product)
