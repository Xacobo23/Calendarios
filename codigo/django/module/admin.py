from django.contrib import admin

from .models import Module

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'fp')
    list_filter = ('code', 'fp')
    search_fields = ('name', )

admin.site.register(Module, ModuleAdmin)

