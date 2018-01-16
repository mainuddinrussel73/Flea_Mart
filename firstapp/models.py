from django.db import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User)

    portfolio = models.URLField(blank=True)
    profilepic = models.ImageField(upload_to='profilepics',blank=True)
    coverpic = models.ImageField(upload_to='overpics',blank=True)
    address = models.TextField(blank=True)
    istimeout = models.BooleanField(default=False);
    
    def __str__(self):
        return self.user.username
    def get_name(self):
        return self.user.username
    def get_some(self):
        return self.profilepic
    def get_absolute_url(self):
        return reverse("username", kwargs={"username": self.user.username})
