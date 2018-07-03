from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Questions(models.Model):
    title = models.CharField(max_length=5000)
    oa = models.CharField(max_length=1000)
    ob = models.CharField(max_length=1000)
    oc = models.CharField(max_length=1000)
    od = models.CharField(max_length=1000)
    ans = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Queadd(models.Model):
    qid = models.OneToOneField(Questions, default=0, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, default=0, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
