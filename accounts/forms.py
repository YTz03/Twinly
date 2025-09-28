from django import forms
from django.core.exceptions import ValidationError
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email
        # normalize and reject spaces
        email = email.strip()
        if ' ' in email:
            raise forms.ValidationError("Email cannot contain spaces.")
        # lower-case for uniqueness
        email_lower = email.lower()
        if User.objects.filter(email__iexact=email_lower).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email_lower

    def clean_first_name(self):
        first = self.cleaned_data.get('first_name', '')
        if ' ' in first:
            raise forms.ValidationError('First name cannot contain spaces.')
        return first

    def clean_last_name(self):
        last = self.cleaned_data.get('last_name', '')
        if ' ' in last:
            raise forms.ValidationError('Last name cannot contain spaces.')
        return last

    def clean_password2(self):
        # Use Django's default password confirmation first
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")

        # Disallow spaces in password
        if password1 and any(ch.isspace() for ch in password1):
            raise forms.ValidationError("Password cannot contain spaces.")

        # Call the model manager's password validation so your custom rules are enforced
        try:
            User.objects.password_validation(password1)
        except ValidationError as e:
            # Convert model ValidationError to a form ValidationError
            raise forms.ValidationError(e.messages)

        return password2