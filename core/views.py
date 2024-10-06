from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib import messages
from posts.models import Post
from .forms import PostForm, UserProfileForm
from .utils.timeUtils import time_since  
from django.db.models import Q
from posts.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePageView(ListView):
    model = Post
    template_name = "homePage.html"
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
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
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detailPost.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_since'] = time_since(self.object.created_at)
        return context

class ExplorerPageView(TemplateView):
    template_name = 'explorer/explorerPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')

        users = []
        posts = []

        if query:
            users = User.objects.filter(username__icontains=query)
            posts = Post.objects.filter(Q(content__icontains=query) | Q(user__username__icontains=query))

        context['query'] = query  
        context['users'] = users
        context['posts'] = posts
        return context
    
class UserProfileView(DetailView):
    model = User
    template_name = 'users/userProfilePage.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(user=self.object).order_by('-created_at')
        context['post_count'] = posts.count()
        context['posts'] = [
            {
                'post': post,
                'time_since': time_since(post.created_at)  
            } for post in posts
        ]
        return context
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/editProfilePage.html'
    success_url = reverse_lazy('userProfilePage', kwargs={'pk': 0}) 

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('userProfilePage', kwargs={'pk': self.request.user.pk}) 