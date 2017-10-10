from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Comment
from .models import Replies

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25,error_messages={'required': 'name'},widget=forms.TextInput(attrs={'placeholder':'Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'From: Gmail'}))
    to = forms.EmailField(error_messages={'required': 'Please enter reciever email'},widget=forms.TextInput(attrs={'placeholder':'To: Email'}))
    comments = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Comment'}), required=False)

    def clean_name(self):
        cd = self.cleaned_data
        if cd.get('name', '') == 'hotmail':
            raise ValidationError("name not allowed")
        return cd.get('name', '')


class TestingForm(forms.Form):
    name = forms.CharField(error_messages={'required':''})
    email = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea)

    def clean_name(self):
        cd = self.cleaned_data
        if cd.get('name') == 'hotmail':
            raise forms.ValidationError("hotmail is not allowed!")
        return cd.get('name')

class CommentForm(forms.ModelForm):

    name = forms.CharField(error_messages={'required':'god i love you'})


    def clean_email(self):
        cd = self.cleaned_data
        if cd.get('email') == 'hotmail@gmail.com':
            raise forms.ValidationError("hot mail not allowed")
        return cd.get('email')

    class Meta:
        model = Comment
        fields = ('name','email','body')


class RepliesForm(forms.ModelForm):
    class Meta:
        model = Replies
        fields = ('name','email','body')