from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
from rest_framework import serializers
from rest_framework import status
from django.contrib import messages

def getArticle(request):
    article = Article.objects.all()
    messages.success(request,"Welcome to the Personal Blog!")
    context = {'data' : article}
    return render(request,'index.html',context)


def addArticle(request):
    if request.method == "POST":
        article_name = request.POST.get('article_name')
        description = request.POST.get('description')
        image = request.FILES.get('blogImg')  # Use request.FILES for file uploads
        tags = request.POST.get('tags')
        
        if Article.objects.filter(article_name=article_name).exists():
            messages.error(request, "Create an article with a different name.")
            return render(request, 'create.html')
        
        Article.objects.create(
            article_name=article_name,
            description=description,
            image=image,
            tags=tags
        )
        messages.success(request, "Article Posted!")
        response = redirect('get_article')  # Ensure 'get_article' URL exists
        print(response)
        return response
        
    return render(request, 'create.html')

def editArticle(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        article_name = request.POST.get('article_name')
        description = request.POST.get('description')
        image = request.POST.get('id_blogImg')
        tags = request.POST.get('tags')

        if Article.objects.exclude(id=id).filter(article_name=article_name).exists():
            messages.error(request, "An article with this name already exists. Please choose a different name.")
            return render(request, 'edit.html', {'article': article})

        article.article_name = article_name
        article.description = description
        article.image = image
        article.tags = tags
        article.save()

        messages.success(request, "Article updated successfully!")
        return redirect('/')  # Redirect to the index or another page

    return render(request, 'edit.html', {'article': article})

def deleteArticle(request,id):
    article = Article.objects.get(id=id)
    article.delete()
    return redirect('/')
