from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # Using EmailField for username
    password = models.CharField(max_length=128)  # Store hashed passwords

    class Meta:
        managed = False
        db_table = 'users'
    def __str__(self):
        return self.email
    

    