from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Note

class NoteEditForm(forms.ModelForm):
    """Form for editing a note. Used on edit_note page."""

    class Meta:
        model = Note
        fields = ['note']
        widgets = {
            'note': forms.TextInput(attrs={'placeholder': 'Enter your task...', 'required': True}),
        }


class ProfileEditForm(forms.ModelForm):
    """Form for editing username and email on the profile page."""

    class Meta:
        model = User
        fields = ['username', 'email']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
