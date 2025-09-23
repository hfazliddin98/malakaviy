from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    """Foydalanuvchi kirish formasi"""
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi nomi'})
    )
    password = forms.CharField(
        label="Parol",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'}),
    )



class RoyxatForm(UserCreationForm):
    """Foydalanuvchi ro'yxat formasi"""
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi nomi'}),
        error_messages={
            'required': 'Foydalanuvchi nomini kiriting',
            'max_length': 'Foydalanuvchi nomi 150 belgidan oshmasligi kerak'
        }
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'}),
        error_messages={
            'required': 'Ismingizni kiriting',
            'max_length': 'Ism 30 belgidan oshmasligi kerak'
        }
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangiz'}),
        error_messages={
            'required': 'Familiyangizni kiriting',
            'max_length': 'Familiya 30 belgidan oshmasligi kerak'
        }
    )
    sharif = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sharifingiz'}),
        error_messages={
            'required': 'Sharifingizni kiriting',
            'max_length': 'Sharif 100 belgidan oshmasligi kerak'
        }
    )
    password1 = forms.CharField(
        label="Parol",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol (kamida 6 ta belgi)'}),
        min_length=6,
        error_messages={
            'required': 'Parolni kiriting',
            'min_length': 'Parol kamida 6 ta belgidan iborat bo\'lishi kerak'
        }
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlash",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni takrorlang'}),
        strip=False,
        error_messages={
            'required': 'Parolni takrorlash majburiy'
        }
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "sharif", "password1", "password2")
        error_messages = {
            'username': {
                'unique': 'Bu foydalanuvchi nomi allaqachon mavjud'
            }
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar mos kelmaydi!")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu foydalanuvchi nomi allaqachon band!")
        return username