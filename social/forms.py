from django import forms
from .models import Post, Comment, MessageModel

class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
        'rows':'3',
        'placeholder':'Write a Post'
        }))

    image = forms.ImageField(
        required = False,
        widget=forms.ClearableFileInput(attrs={
        'multiple':True
        }))
    class Meta:
        model = Post
        fields = ['body']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
        'rows':'2',
        'placeholder':'What do you think about this post?'
        }))
    class Meta:
        model = Comment
        fields = ['comment']

class ThreadForm(forms.Form):
    username = forms.CharField(label='',max_length=50)

class MessageForm(forms.ModelForm):
    # body = forms.CharField(label='',max_length=1000)
    image = forms.ImageField(label='',required = False)
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
        'rows':'1',
        'placeholder':'Type your messages'
        }))
    class Meta:
        model = MessageModel
        fields = ['body','image']

class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
        'rows':'3',
        'placeholder':'Qoute this Post'
        }))

class ExploreForm(forms.Form):
    query = forms.CharField(
        label = '',
        widget=forms.TextInput(attrs={
            'placeholder':'Explore Tags'
        })
    )
