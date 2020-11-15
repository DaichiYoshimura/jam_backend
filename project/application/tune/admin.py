from django.contrib import admin
from .models import Tune


@admin.register(Tune)
class TuneAdmin(admin.ModelAdmin):
    pass
