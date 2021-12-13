from django.db import models

# Create your models here.
# models.py
class PostAudio(models.Model):
    hotel_Main_Img = models.ImageField(upload_to='static/media/')
    description = models.TextField(null=True)

