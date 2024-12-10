from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import date

class Blogs(models.Model):
    name = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=100)
    post_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)