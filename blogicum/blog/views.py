from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from .constants import POSTS_ON_PAGE
from .forms import CommentForm
from .mixins import (
    CreateUpdateComment, CreateUpdatePost, PostMixin, CommentMixin,
    OnlyAuthorMixin
)
from .models import Category, Comment, Post, User
from .utils import count_comments, paginate_queryset


class IndexListView(ListView):
    """Начальная страница Блогикума."""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self):
        return count_comments(Post.published_objects.all())


class PostDetailView(DetailView):
    """Страница отдельного поста."""

    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_object(self):
        post_on_page = get_object_or_404(Post, id=self.kwargs['post_id'])
        if self.request.user == post_on_page.author:
            post = post_on_page
        else:
            post = get_object_or_404(Post.published_objects.all(),
                                     id=self.kwargs['post_id'])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['form'] = CommentForm(self.request.POST or None)
        context['comments'] = self.get_object().comments.order_by('created_at')
        return context


class CategoryListView(ListView):
    """Публикации отдельной категории."""

    model = Post
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def get_object(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return category

    def get_queryset(self):
        page_obj = count_comments(
            Post.published_objects.all()
            .select_related('category',)
            .filter(category__slug=self.kwargs['category_slug'])
        )
        page_obj = paginate_queryset(self.request, page_obj, POSTS_ON_PAGE)
        return page_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        context['page_obj'] = self.get_queryset()
        return context


class UserDetailView(DetailView):
    """Посты отдельного пользователя."""

    model = User
    template_name = "blog/profile.html"

    def get_object(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username']
        )

    def get_queryset(self):
        if self.request.user == self.get_object():
            page_obj = count_comments(
                Post.objects.filter(author=self.get_object().id).
                order_by('-pub_date')
            )
        else:
            page_obj = count_comments(
                Post.published_objects.all().filter(
                    author=self.get_object().id)
            )

        return paginate_queryset(self.request, page_obj, POSTS_ON_PAGE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        context['page_obj'] = self.get_queryset()
        return context


class PostCreateView(LoginRequiredMixin, PostMixin, CreateUpdatePost,
                     CreateView):
    """Создание поста."""

    pass


class PostUpdateView(OnlyAuthorMixin, PostMixin, CreateUpdatePost, UpdateView):
    """Редактирование поста."""

    pk_url_kwarg = 'post_id'


class PostDeleteView(PostMixin,
                     OnlyAuthorMixin, DeleteView):
    """Удаление поста."""

    pass


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateUpdateComment,
                        CreateView):
    """Создание комментария."""

    pk_url_kwarg = 'post_id'


class CommentUpdateView(LoginRequiredMixin, CreateUpdateComment, CommentMixin,
                        OnlyAuthorMixin, UpdateView):
    """Редактирование комментария."""

    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post,
                                            pk=self.kwargs['post_id'])
        context['comment'] = get_object_or_404(Comment,
                                               pk=self.kwargs['comment_id'])
        return context


class CommentDeleteView(LoginRequiredMixin, OnlyAuthorMixin, CommentMixin,
                        DeleteView):
    """Удаление комментария."""

    pk_url_kwarg = 'comment_id'

    def get_object(self):
        return get_object_or_404(Comment, pk=self.kwargs['comment_id'])


class EditProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля."""

    model = User
    fields = ('username', 'first_name', 'last_name', 'email',)
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.get_object()})
