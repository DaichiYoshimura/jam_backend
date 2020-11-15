from django.contrib import admin
from .models import Performance


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    pass
