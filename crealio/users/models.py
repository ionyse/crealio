from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site


class User(AbstractUser):
    site = models.ForeignKey(Site)

    address1 = models.CharField('address 1', max_length=100, blank=True)
    address2 = models.CharField('address 2', max_length=100, blank=True)
    zipcode = models.CharField('zip code', max_length=10, blank=True)
    city = models.CharField('city', max_length=75)
    country = models.CharField('country', max_length=75)

    dob = models.DateField('date of birth', null=True, blank=True)
    pob = models.CharField('city of birth', max_length=75, blank=True)
    country = models.CharField('country of birth', max_length=75)

    nationality = models.CharField('nationality', max_length=75, blank=True)

    GENDER = (
        ('M', 'male'),
        ('F', 'female'),
        ('O', 'other'),
    )
    sex = models.CharField('gender', choices=GENDER, max_length=1, blank=True)

    d_licence = models.CharField('driver licence', max_length=100, blank=True)

    phone = models.CharField('landline', max_length=20, blank=True)
    mobile = models.CharField('mobile', max_length=20, blank=True)
    job = models.CharField('job title', max_length=50)
    identite = models.ImageField('picture', upload_to="identite", blank=True)

    def __str__(self):
        return str(self.user)
