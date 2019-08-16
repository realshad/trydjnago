from django.db import models
# Create your models here.

class Car(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(upload_to='cars')

def content_file_name(instance, filename):
    return '/'.join(['content', instance.user.username, filename])

class Content(models.Model):
    name = models.CharField(max_length=200)
    #user = models.ForeignKey(User)
    file = models.FileField(upload_to=content_file_name)