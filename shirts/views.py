from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.paginator import Paginator
from .models import Shirt, Comment
from .forms import ShirtForm
from fpdf import FPDF
from shop.settings import MEDIA_ROOT
from PIL import Image
from io import BytesIO
import img2pdf
import requests
from django.contrib.auth.models import User
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
import base64
import re



def split_objects_in_queryset(queryset):
    result = []
    i = 0
    line = []
    for obj in queryset:
        if i % 3 == 0 and i != 0:
            result.append(line)
            line = []
        line.append(obj)
        i = i+1
    if line.__len__():
        result.append(line)
    return result


def upload(request):
    if request.user.is_staff:
        context = {'form': ShirtForm()}
        if request.method == 'POST':
            form = ShirtForm(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                form.save()
        return render(request, 'upload.html', context)
    else:
        return render(request, 'not_found.html')




def index(request):
    queryset_list = Shirt.objects.filter(author__is_staff=True).order_by('id')
    # table = splitobjectsinqueryset(queryset)
    paginator = Paginator(queryset_list, 18)

    page = request.GET.get('page')
    if not page:
        page = 1
    queryset = paginator.get_page(page)
    queryset.object_list = split_objects_in_queryset(queryset.object_list)
    context = {'Shirts': queryset}
    return render(request, 'index.html', context)


def shirt_detail_page(request, shirt_id):
    shirt = Shirt.objects.get(id=shirt_id)
    context = {'shirt': shirt}
    return render(request, 'shirt_detail.html', context)


def get_comment(request):
    shirt_id = int(request.GET['id'])
    comments = Comment.objects.filter(shirt__id=shirt_id)
    commentsJSON = []
    for comment in comments:
        commentsJSON.append({"user": comment.author.username,
                             "user_id": comment.author.id,
                             "text": comment.text,
                             "likes": comment.likes.count(),
                             "id": comment.id,
                             },)
    return JsonResponse(commentsJSON, safe=False)


def setLike(comment, current_user):
    if current_user in comment.likes.all():
        comment.likes.remove(current_user)
    else:
        comment.likes.add(current_user)


def like_comment(request):
    current_user = request.user
    data = request.POST
    if current_user.is_authenticated:
        comment_id = int(data['id'])
        comment = Comment.objects.get(pk=comment_id)
        setLike(comment, current_user)
        return JsonResponse([{"result": comment.likes.count()}], safe=False)
    else:
        return JsonResponse([{"result": "You are not authenticated"}], safe=False)


def add_comment(request):
    data = request.POST
    shirt_id = int(data['id'])
    text = data['text']
    current_user = request.user
    if current_user.is_authenticated:
        Comment.objects.create(shirt_id=shirt_id, author_id=current_user.id, text=text)
    else:
        return JsonResponse([{"result": "You are not authenticated"}])
    return JsonResponse([{"result": "Ok"}], safe=False)


def remove_transparency(im, bg_colour=(255, 255, 255)):
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        alpha = im.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg
    else:
        return im


def get_bytes_to_pdf(img):
    img_arr = BytesIO()
    img = remove_transparency(img)
    img.convert("RGB").save(img_arr, format='JPEG')
    img_arr = img_arr.getvalue()
    return img_arr


def download_image(request, shirt_id):
    shirt = Shirt.objects.get(id__exact=shirt_id)
    shirt_url = shirt.image.build_url()
    response = requests.get(shirt_url)
    img = Image.open(BytesIO(response.content))
    pdf_bytes = img2pdf.convert(get_bytes_to_pdf(img))
    file = open(MEDIA_ROOT+"/download.pdf", "wb")
    file.write(pdf_bytes)
    img.close()
    file.close()
    return FileResponse(open(MEDIA_ROOT+"/download.pdf", "rb"), as_attachment=True,
                        filename="shirt.pdf", content_type="application/pdf")


def constructor(request):
    return render(request, "constructor.html")


def constructor_upload(request):
    data = request.POST
    print(data.get('description'))
    print(data.get('image'))
    base64_data = re.sub('^data:image/.+;base64,', '', data.get('image'))
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    if not request.user.is_authenticated:
        return JsonResponse({"result": "error"})
    user = request.user
    shirt = Shirt.objects.create(title=data.get('title'), description=data.get('description'), author=user)
    shirt.image = cloudinary.uploader.upload_resource(image_data).build_url()
    shirt.save()
    print(data.get('title'))
    print(data.get('description'))
    return JsonResponse({"result": "uploaded"})


def order_view(request):
    shirt = Shirt.objects.get(id__exact=int(request.POST.get("shirt-id")))
    context = {"shirt": shirt.title,
               "sex": request.POST.get("sex"),
               "size": request.POST.get("size")}
    if not len(request.POST.dict()):
        context = {}
    return render(request, "order.html", context)
