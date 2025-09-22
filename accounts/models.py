from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    date_of_birth = models.DateField(null=True, blank=True)

    RELATIONSHIP_STATUS = [
        ('single', 'רווק/ה'),
        ('in_relationship', 'במערכת יחסים'),
        ('married', 'נשוי/אה'),
    ]
    relationship_status = models.CharField(max_length=20, choices=RELATIONSHIP_STATUS, default='single')

    partner = models.CharField(max_length=150, blank=True, null=True)

    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username