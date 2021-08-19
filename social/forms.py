from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
        'rows':'3',
        'placeholder':'Write a Post'
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
