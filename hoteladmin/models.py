from django.db import models

# Create your models here.

class USER(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=50)
    designation = models.CharField(max_length=20)

    def __str__(self):
        return self.username + " | " + self.designation