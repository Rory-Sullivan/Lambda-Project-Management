from django import forms


class DateWidget(forms.TextInput):
    input_type = "date"


class DurationWidget(forms.TextInput):
    input_type = "time"

    def value_from_datadict(self, data, files, name):
        raw_value = super().value_from_datadict(data, files, name)
        (hours, minutes) = raw_value.split(":")
        return f"00 {hours}:{minutes}:00.0"
