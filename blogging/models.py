from django.db import models

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    article_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to = '', null=True)
    pub_date = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200)

