from django import forms
from kjgramm.models import Photo


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False)


class PhotoModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["file"]
