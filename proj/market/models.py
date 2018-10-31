from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

def get_path(instance,filename):
	return '{0}/{1}'.format(instance.title,filename)


class Post(models.Model):
    pub_date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    desc = models.TextField() #this is the book description
    cost=models.FloatField(default=0)
    file=models.FileField(upload_to=get_path,null=True)
    image=models.FileField(upload_to=get_path,null=True)

    def publish(self):
 #       self.pub_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Customer(models.Model):
	user=models.ForeignKey(User)
	book=models.ManyToManyField(Post)

	def __str__(self):
		return self.user.username
