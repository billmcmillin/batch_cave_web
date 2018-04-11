from django import forms
from converter.models import Conversion

UNNAMED_CONVERSION_ERROR = "Conversion must have a name."
UNTYPED_CONVERSION_ERROR = "You must select a type."
NOFILE_CONVERSION_ERROR = "Conversion must have a valid MARC file."

class ConversionForm(forms.ModelForm):
    class Meta:
        model = Conversion
        fields = ('Name', 'Type', 'Upload',)
        widgets = {
            'Name': forms.fields.TextInput(attrs={
                'placeholder': 'Give it a name',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'Name': {'required': UNNAMED_CONVERSION_ERROR},
            'Type': {'required': UNTYPED_CONVERSION_ERROR},
            'Upload': {'required': NOFILE_CONVERSION_ERROR},
        }
