from django.contrib import admin

from .models import FP

class FPAdmin(admin.ModelAdmin):
    list_display = ('name', 'fp_type', 'description')
    list_filter = ('fp_type', )
    search_fields = ('name', )

    class Meta:
        verbose_name = 'Ciclo Formativo'
        verbose_name_plural = 'Ciclos Formativos'

admin.site.register(FP, FPAdmin)

