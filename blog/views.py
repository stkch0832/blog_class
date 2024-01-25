from django.shortcuts import render
from accounts.models import User, Profile
from .models import Post
from .forms import BlogForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages


class BlogListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BlogCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = BlogForm
    template_name = 'blog/blog_form.html'

    success_message = "%(title)s を新規投稿しました。"
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(BlogCreateView, self).form_valid(form)


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'


class BlogUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_message = "%(title)s を更新しました。"

    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={
            'pk': self.kwargs['pk'],
        })


class BlogDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:blog_list')
    success_message = "投稿を削除しました。"
