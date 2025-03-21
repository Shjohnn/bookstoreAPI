import os
from tkinter.constants import CASCADE

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Account(AbstractUser):
    image = models.ImageField(upload_to='accounts/', null=True, blank=True)

    def __str__(self):
        return self.username


class Book(models.Model):
    title=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    details=models.TextField(blank=True, null=True)
    price=models.FloatField(validators=[MinValueValidator(0.0)])
    cover=models.CharField(max_length=50, blank=True,null=True)
    sold=models.BooleanField(default=False)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Image(models.Model):
    image=models.ImageField(upload_to='books/')
    book =  models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title

    def delete(self,*args,**kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args,**kwargs)

# @receiver(post_delete, sender=Image))
# def delete_file(sender,instance, **kwargs):
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             os.remove(instance.image)
#


class Wishlist(models.Model):
    account= models.OneToOneField(Account, on_delete=models.CASCADE)
    books= models.ManyToManyField(Book)

    def __str__(self):
        return self.account.username