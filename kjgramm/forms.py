from django import forms
from kjgramm.models import Photo


class TextForm(forms.Form):
    text = forms.CharField(max_length=50)


class PhotoModelForm(forms.ModelForm):
    class Meta:
        model = Photo
