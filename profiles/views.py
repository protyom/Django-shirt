from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .forms import SignupForm
from shirts.models import Shirt, Comment
import re


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        is_valid = form.is_valid()
        match = re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.]+$", form.cleaned_data.get("email"))
        if is_valid and match:
            to_email = form.cleaned_data.get('email')
            emails = User.objects.filter(email=to_email)
            if emails.count() > 0:
                form.add_error("email", "User with this email already exists")
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your SHIrT account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.content_subtype = "html"
                email.send()
                return render(request, 'registration/check_email.html')
        if not match:
            form.add_error("email", "Wrong email")
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'registration/verified.html')
    else:
        return HttpResponse(request, 'not_found.html')


def personal(request, user_id):
    if not request.user.is_authenticated:
        return request(request, 'not_found.html')
    shirts = Shirt.objects.filter(author_id=user_id)
    awards = []
    if Comment.objects.filter(author_id=user_id).count() >= 5:
        awards.append("Leave 5 comments")
    if Shirt.objects.filter(author_id=user_id).count() >= 5:
        awards.append("Make 5 designs")
    num = Comment.objects.filter(likes__id=user_id)
    if num.count() >= 5:
        awards.append("Like 5 comments")
    if len(awards) == 3:
        awards.append("SHIrT veteran")
    if shirts.count() == 0:
        shirts = None
    user = User.objects.get(id__exact=user_id)
    context = {
        "user_name": user.username,
        "shirts": shirts,
        "awards": awards,
    }
    return render(request, 'personal.html', context)
