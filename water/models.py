from django.db import models
from django.contrib.auth.models import  User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Brand(models.Model):
    brand = models.CharField(max_length=100)
    brand_logo = models.FileField()

    def __str__(self):
        return self.brand


class Quality(models.Model):
    brand_info = models.ForeignKey(Brand, on_delete=models.CASCADE , null=True)
    size = models.IntegerField(default=1)
    price = models.IntegerField(default=10)

    def __str__(self):
        return  (str(self.brand_info) +' - '+str(self.size))

class ZipCode(models.Model):
    pin_code = models.CharField(max_length=6, default=111111)

    def __str__(self):
        return self.pin_code
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=300, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    pin_code = models.CharField(max_length=6, null=True)
    mobile_no = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.user.username


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
