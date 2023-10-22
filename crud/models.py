from django.db import models
from django.utils import timezone

# Create your models here. Tables created here will be created in the database

#Roles models
#Table Roles
class Roles(models.Model):
    rol_name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    create_date = models.DateTimeField(default=timezone.now)
    rol_status = models.BooleanField(default=True)

    def __str__(self) :
        return self.rol_name

# Define the Users model
#Table Users
class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    type_document = models.CharField(max_length=20)
    document = models.PositiveSmallIntegerField(unique=True) #TODO: add unique
    birthday = models.DateField()
    phone_number = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)
    register_date = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=60)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='users')
    password = models.CharField(max_length=30, null=True, blank=True)
    #user_image = models.ImageField(upload_to='images/', default='https://azusersimages16.blob.core.windows.net/images1az/defect_image.png',null=True, blank=True)
    user_image = models.CharField(max_length=200, null=True, default='https://azusersimages16.blob.core.windows.net/images1az/defect_image.png', blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
