from django.contrib import admin
from .models import Article
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display =['article_name','pub_date','last_modified','tags']
    
admin.site.register(Article, ArticleAdmin)