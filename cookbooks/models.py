from django.db import models
from django.conf import settings

class Cookbook(models.Model):
    title = models.CharField(max_length=55)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(to='tags.tag', related_name='cookbooks', blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
