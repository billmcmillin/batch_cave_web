from django import forms
from converter.models import Conversion


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
