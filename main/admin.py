from django.contrib import admin

from .models import *
admin.site.register(Book)
admin.site.register(Account)
admin.site.register(Image)
admin.site.register(Wishlist)