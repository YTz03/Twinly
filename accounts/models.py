from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# create custom user model with additional fields containing: full name, date of birth, email, relationship status, password and then generate the user unique id automatically
class UserManager(BaseUserManager): 
    def create_user(self, email, password, first_name, last_name, date_of_birth, **additional_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)

        try:    
            validate_email(email)
        except ValidationError:
            raise ValueError("Invalid email address")
        
        try:
            self.model.objects.get(email=email)
            raise ValueError("Email address already in use")
        except self.model.DoesNotExist:
            pass

        try:
            if self.password_validation(password):
                pass
        except ValidationError as e:
            raise ValueError(f"Password validation error: {e}")

        if len(first_name) < 2 or len(first_name) > 15 or ' ' in first_name:
            raise ValueError("First name must be between 2 and 15 characters long and cannot contain spaces")

        if len(last_name) < 2 or len(last_name) > 15 or ' ' in last_name:
            raise ValueError("Last name must be between 2 and 15 characters long and cannot contain spaces")

        if date_of_birth is None or date_of_birth == '':
            raise ValueError("Date of birth is required")
        elif date_of_birth >= datetime.today().date():
            raise ValueError("Date of birth must be in the past")

        user = self.model(email=email, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, **additional_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def password_validation(self, password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        elif not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit")
        elif not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least one letter")
        elif not any(char in "!@#$%^&*()-+" for char in password):
            raise ValidationError("Password must contain at least one special character")

        return True

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    choices=[
        ('single', 'Single'),
        ('in_a_relationship', 'In a Relationship'),
    ]
    relationship_status = models.CharField(max_length=50, choices=choices, default='single')

    partner = models.EmailField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']  # password is handled separately by Django

    def __str__(self):
        return self.email