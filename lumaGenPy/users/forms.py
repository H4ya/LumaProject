from django import forms
from .models import User ,Students
from django.contrib.auth.forms import AuthenticationForm
  

class SignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')
    email = forms.EmailField(max_length=50, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    class Meta:
        model = Students 
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Students.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password
    
class LoginForm(AuthenticationForm):
    email = forms.EmailField(label="Email", max_length=254)  
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AuthenticationForm
        fields = ['email', 'password']    