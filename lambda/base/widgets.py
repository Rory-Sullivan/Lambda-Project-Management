from django import forms
import re

HOUR_MINUTE = re.compile("^([0-1][0-9]|[2][0-3]):([0-5][0-9])$")
HOUR_MINUTE_SECOND = re.compile(
    "^([0-1][0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])$"
)


class DateWidget(forms.TextInput):
    input_type = "date"


class DurationWidget(forms.TextInput):
    input_type = "time"

    def value_from_datadict(self, data, files, name):
        time_val = super().value_from_datadict(data, files, name)

        if HOUR_MINUTE.match(time_val):
            return time_val + ":00"
        if HOUR_MINUTE_SECOND.match(time_val):
            return time_val
        return None
