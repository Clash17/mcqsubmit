from django.db import models

from django.contrib.auth.models import User


class Player(models.Model):
    fname1 = models.CharField(max_length=44)
    lname1 = models.CharField(max_length=44)
    fname2 = models.CharField(max_length=44)
    lname2 = models.CharField(max_length=44)
    uid = models.OneToOneField(User, default=0, on_delete=models.CASCADE)

    def __str__(self):
        return self.fname1 + " " + self.fname2


# Create your models here.
class Questions(models.Model):
    title = models.CharField(max_length=1000)
    ans = models.IntegerField(default=0)
    code = models.CharField(max_length=5000, default=None)

    def __str__(self):
        return self.title


class Queadd(models.Model):
    qid = models.OneToOneField(Questions, default=0, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, default=0, on_delete=models.CASCADE)

    def __str__(self):
        return self.qid.title


class Stream(models.Model):
    uid = models.OneToOneField(User, default=0, on_delete=models.CASCADE)
    choice = models.IntegerField(default=0)

    def __str__(self):
        m = " Not yet"
        if self.choice == 1:
            m = " Front End "
        elif self.choice == 2:
            m = " Back End "
        return self.uid.first_name + m
