from django import forms


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class DatePickerInput(forms.DateTimeInput):
    input_type = 'date'
