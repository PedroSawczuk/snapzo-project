from django import forms
from posts.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content'] 
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Escreva seu post...', 'rows': 4}),
        }
