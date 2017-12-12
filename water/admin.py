from django.contrib import admin
from .models import Brand, Quality, UserProfile, ZipCode


admin.site.register(Brand)
admin.site.register(Quality)
admin.site.register(UserProfile)
admin.site.register(ZipCode)
