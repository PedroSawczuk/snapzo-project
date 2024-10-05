from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from posts.models import Post
from .forms import PostForm
from .utils.timeUtils import time_since  

class HomePageView(ListView):
    model = Post
    template_name = "homePage.html"
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        # Retorna todos os posts, independentemente do número
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        context['posts'] = [
            {
                'post': post,
                'time_since': time_since(post.created_at)
            } for post in self.object_list
        ]
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar autenticado para fazer um post.")
            return redirect('homePage') 

        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
            post.save()
            return redirect('homePage')
        return self.get(request, *args, **kwargs)
