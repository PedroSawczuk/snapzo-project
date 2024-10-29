from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.contrib import messages
from notifications.models import Notification
from posts.models import Like, Post
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

        form = PostForm(request.POST, request.FILES) 
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
        context['has_liked'] = self.request.user.is_authenticated and self.object.likes.filter(user=self.request.user).exists()
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
        context['current_user'] = self.request.user if self.request.user.is_authenticated else None
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
    
class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/editPost.html'  
    success_url = reverse_lazy('homePage')

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/deletePost.html' 
    success_url = reverse_lazy('homePage')

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()  
            action = 'unliked'
            Notification.objects.filter(user=post.user, post=post, message=f"{request.user.username} curtiu seu post").delete()
        else:
            action = 'liked'
            post_url = reverse('postDetailPage', args=[post.id]) 
            Notification.objects.create(
                user=post.user,
                post=post,
                message=f"{request.user.username} curtiu seu post",
                post_url=post_url  
            )

        post.like_count = post.likes.count() 
        post.save()
        
        return JsonResponse({'action': action, 'like_count': post.like_count})

class NotificationPageView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notificationsPage.html'
    context_object_name = 'notifications'
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_at')
        posts_data = [
            {
                'id': post.id,
                'content': post.content,
                'username': post.user.username,
                'time_since': time_since(post.created_at),
            }
            for post in posts
        ]
        return JsonResponse(posts_data, safe=False)