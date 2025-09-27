from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User
from datetime import date

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        
class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'relationship_status')
        
    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        if dob >= date.today():
            raise forms.ValidationError("Date of birth must be in the past")
        return dob