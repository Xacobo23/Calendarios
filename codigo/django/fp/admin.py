from django.contrib import admin

from .models import FP

class FPAdmin(admin.ModelAdmin):
    list_display = ('name', 'fp_type', 'description')
    list_filter = ('fp_type', )
    search_fields = ('name', )

admin.site.register(FP, FPAdmin)

