from django.db import models

# Create your models here.

class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    head0 = models.CharField(max_length=90000000)
    chead0 = models.CharField(max_length=98669876787)
    head1 = models.CharField(max_length=7462646)
    chead1 = models.CharField(max_length=9374854877846)
    head2 = models.CharField(max_length=5767576865)
    chead2 = models.CharField(max_length=89347427374)
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to = "blog/images" , default = " ")

    def __str__(self) :
        return self.title