# shifts/forms.py
from django import forms
from .models import Shift
from datetime import datetime, timedelta


class ShiftForm(forms.ModelForm):
    start_time = forms.CharField(max_length=5)  # 文字列として受け取る
    end_time = forms.CharField(max_length=5) 
    class Meta:
        model = Shift
        fields = ['name', 'date', 'start_time', 'end_time']

"""    def clean_start_time(self):
        start_time_str = self.cleaned_data.get('start_time')#文字列から時間に変換
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
        except ValueError:
            raise forms.ValidationError("有効な出勤時間を入れて。")
        return start_time_str

    def clean_end_time(self):
        end_time_str = self.cleaned_data.get('end_time')
        try:
            hours, minutes = map(int, end_time_str.split(':'))
            if hours >= 24:
                hours -= 24
            end_time = (datetime.min + timedelta(hours=hours, minutes=minutes)).time()
        except ValueError:
            raise forms.ValidationError("有効な退勤時間を入れて。")
        return end_time_str

    def clean(self):
        cleaned_data = super().clean()
        start_time_str = cleaned_data.get("start_time")
        end_time_str = cleaned_data.get("end_time")

        if start_time_str and end_time_str:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            hours, minutes = map(int, end_time_str.split(':'))
            if hours >= 24:
                hours -= 24
            end_time = (datetime.min + timedelta(hours=hours, minutes=minutes)).time()

            if start_time > end_time:
                raise forms.ValidationError("有効な時間を入れて")
        return start_time_str"""
