from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email
    
class LoginForm(AuthenticationForm):
    email = forms.EmailField(label="Email", max_length=254)  
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AuthenticationForm
        fields = ['username', 'password']    