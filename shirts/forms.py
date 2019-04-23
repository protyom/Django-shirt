from .models import Shirt
from django.forms import ModelForm


class ShirtForm(ModelForm):
    class Meta:
        model = Shirt
        fields = "__all__"
