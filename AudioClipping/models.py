from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-
from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
