from django import forms
from kjgram.models import Photo


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False)


class CommentForm(forms.Form):
    text = forms.CharField()

class PhotoModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["file"]
