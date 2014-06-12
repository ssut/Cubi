from django.db import models

class Value(models.Model):
    d_day = models.DateTimeField()

class Artwork(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='teaser/')

    def __unicode__(self):
        return self.title

class Introduce(models.Model):
    description = models.TextField(blank=True)
    cartoon = models.ImageField(upload_to='teaser/')
    mail_description = models.TextField(blank=True)
