from django.db import models
import os
from uuid import uuid4

# Create your models here.

def rename_photo(instance, filename):
    upload_to = 'user'
    ext = filename.split('.')[-1]
    # get filename
    if instance.u_id:
        filename = '{}.{}'.format(instance.u_id, ext)
    else:
        # set filename as random string
         filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
    # return "%s/%s" %(instance.Name,filename)
class Users(models.Model):
    u_id = models.CharField(max_length=10)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    role = models.CharField(max_length=70)
    dsgn = models.CharField(max_length=70)
    img = models.ImageField(upload_to=rename_photo, null=True, blank=True)

    def __str__(self):
        return self.u_id

    def delete(self, *args, **kwargs):
        self.img.delete()
        super().delete(*args, **kwargs)



class attendance(models.Model):
    u_id = models.CharField(max_length=20)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=150)
    def __str__(self):
        return self.u_id


class Setcamera(models.Model):
    dpt_id = models.CharField(max_length=10)
    ip_address=models.CharField(max_length=250)
    camera_num = models.CharField(max_length=50,default="")

    def __str__(self):
        return self.ip_address