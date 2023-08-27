from django.contrib import admin

from .models import NewData, Unit, PipeData

# Register your models here.
admin.site.register(NewData)
admin.site.register(Unit)
admin.site.register(PipeData)
