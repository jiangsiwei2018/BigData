from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=50)
    passwd = models.CharField(max_length=100)

    def __str__(self):
        return "user table: %s " % self.name

    class Meta:
        app_label = "default"


class Book(models.Model):
    user = models.ForeignKey("Users", on_delete=models.CASCADE)
    bookname = models.CharField(max_length=100)

    def __str__(self):
        return "%s: %s" % (self.user.username, self.bookname)

    class Meta:
        app_label = "app_db"
