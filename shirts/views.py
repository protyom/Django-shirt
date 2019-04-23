from django.shortcuts import render
from django.http import JsonResponse
from .models import Shirt, Comment
from .forms import ShirtForm
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api


def splitobjectsinqueryset(queryset):
    result = []
    i = 1
    line = []
    for obj in queryset:
        line.append(obj)
        if i % 2 == 0:
            result.append(line)
            line = []
        i = i+1
    if line.__len__():
        result.append(line)
    return result


def upload(request):
    context = {'form': ShirtForm()}
    if request.method == 'POST':
        form = ShirtForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            form.save()
    return render(request, 'upload.html', context)


def index(request):
    queryset = Shirt.objects.all()
    table = splitobjectsinqueryset(queryset)
    context = {'Shirts': table}
    return render(request, 'index.html', context)


def shirt_detail_page(request, shirt_id):
    shirt = Shirt.objects.get(id=shirt_id)
    comments = shirt.comments.all()
    context = {'shirt': shirt, 'comments': comments}
    return render(request, 'shirt_detail.html', context)


def get_comment(request):
    shirt_id = int(request.GET['id'])
    comments = Comment.objects.filter(shirt__id=shirt_id)
    commentsJSON = []
    for comment in comments:
        commentsJSON.append({"user": comment.author.username,
                             "text": comment.text,
                             "likes": comment.likes.count()})
    return JsonResponse(commentsJSON, safe=False)
