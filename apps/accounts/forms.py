from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm, LoginForm
from .models import UserProfile

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-input'})
        self.fields['password'].widget.attrs.update({'class': 'form-input'}) 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'phone_number', 'address']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }