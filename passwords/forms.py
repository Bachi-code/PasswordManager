from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from passwords.models import PasswordEntry
from cryptography.fernet import Fernet


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')


class PasswordCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordCreate, self).__init__(*args, **kwargs)

    class Meta:
        model = PasswordEntry
        fields = ('site_url', 'password', 'login',)

        widgets = {
            "password": forms.PasswordInput(attrs={'placeholder': '********', 'autocomplete': 'new-password',
                                                   'data-toggle': 'password'}),
            "site_url": forms.URLInput(attrs={'autocomplete': 'new-password'}),
        }

    def clean_password(self):
        password_decrypted = self.cleaned_data['password']
        key = self.user.userkeys.userkey
        cipher = Fernet(key.encode())
        password_en = cipher.encrypt(str.encode(password_decrypted))
        password = password_en.decode('utf-8')
        return password



