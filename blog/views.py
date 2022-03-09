from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from math import ceil
from . models import Blogpost
import json

def index(request):
    blog = Blogpost.objects.all()
    print(blog)
    return render(request , 'blog/index.html', {'blog': blog})

def blogpost(request , id ):
    blogpost = Blogpost.objects.filter(post_id = id )
    return render(request , 'blog/blogpost.html', {'blogpost': blogpost})
    
