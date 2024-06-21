from django import forms
from django.core.exceptions import ValidationError

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'file']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        file = cleaned_data.get('file')

        if not text.strip() and not file:
            raise ValidationError('Сообщение не может быть пустым.')

        return cleaned_data