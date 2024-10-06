from django.contrib.auth.models import User
from django import forms
from posts.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content'] 
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Escreva seu post...', 'rows': 4}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  