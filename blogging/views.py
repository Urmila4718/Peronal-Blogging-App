from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
from rest_framework import serializers
from rest_framework import status
from django.contrib import messages
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
api_key = os.getenv('NEWS_API_KEY')

import requests
def latestArticles(request):
    try:
        url = f'https://newsapi.org/v2/everything?q=general&apiKey={api_key}'
        print('url:',url)
        all_articles = requests.get(url).json()
        a = all_articles['articles']
        desc =[]
        title =[]
        img =[]
        url =[]
        for i in range(len(a)):
            f = a[i]
            title.append(f['title'])
            desc.append(f['description'])
            img.append(f['urlToImage'])
            url.append(f['url'])
            mylist = zip(title, desc, img,url)

        context = {'mylist': mylist}
        print(mylist)
        return render(request, 'news.html', context)

    
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)


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
        
        if image is None:
            image = "default.png"
            print("img::",image)
        Article.objects.create(
            article_name=article_name,
            description=description,
            image=image,
            tags=tags)

                    
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


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

def contact(request):
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Form validation (Optional, can also use Django forms for more robust validation)
        if not name or not email or not subject or not message:
            messages.error(request, "All fields are required!")
            return redirect('contact')

        # Send an email (you can configure settings for email in settings.py)
        try:
            send_mail(
                subject=f'Contact Form: {subject}',
                message=f'From: {name}\nEmail: {email}\n\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('contact')

        return redirect('contact')

    return render(request, 'contact.html')
