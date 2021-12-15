from django.contrib import admin
from .models import Equipment, Category, Status, UserProfile
from tinymce.widgets import TinyMCE
from django.db import models


# Register your models here.

class StatusAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {'fields': ["status_title", "status_published"]}),
        ("URL", {'fields': ["status_slug"]}),
        ("Series", {'fields': ["status_equipment"]}),
        ("Conteúdo", {'fields': ["status_content"]}),
        ("Imagem", {'fields': ['status_image']})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(Equipment)
admin.site.register(Category)
admin.site.register(Status) #, StatusAdmin)
admin.site.register(UserProfile)
