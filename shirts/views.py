from django.shortcuts import render
from .models import Shirt


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


def index(request):
    queryset = Shirt.objects.all()
    table = splitobjectsinqueryset(queryset)
    context = {'Shirts': table}
    return render(request, 'index.html', context)


def shirt_detail_page(request, shirt_id):
    shirt = Shirt.objects.get(id=shirt_id)
    context = {'shirt': shirt}
    return render(request, 'shirt_detail.html', context)
