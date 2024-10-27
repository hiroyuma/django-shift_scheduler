from django.contrib import admin
from.models import Shift

# デフォルトの並べ替えを日付順に設定
class Shiftadmin(admin.ModelAdmin):
    ordering = ['shift_date']
    list_display = ('name', 'shift_date', 'start_time', 'end_time')
    search_fields = ['name']
    list_filter = ['shift_date']

admin.site.register(Shift, Shiftadmin)
