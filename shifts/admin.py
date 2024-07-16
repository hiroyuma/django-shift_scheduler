from django.contrib import admin
from.models import Shift

# デフォルトの並べ替えを日付順に設定
class Shiftadmin(admin.ModelAdmin):
    ordering = ['date']
    list_display = ('name', 'date', 'start_time', 'end_time')
    search_fields = ['name']
    list_filter = ['date']

admin.site.register(Shift, Shiftadmin)
