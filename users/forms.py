from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import User


class RegisterForm(forms.ModelForm):
    """
    Registration form for new citizens.
    password and password2 are not on the model — we handle them manually
    so we can validate they match before saving.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        validators=[validate_password]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'national_id', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'national_id': forms.TextInput(attrs={'placeholder': 'National ID (optional)'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number (optional)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        # This is where mismatched passwords get caught before hitting the DB
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError({'password2': 'Passwords do not match.'})
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Always use set_password — never store plain text
        user.set_password(self.cleaned_data['password'])
        user.role = 'citizen'  # Web registration is always citizen
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
