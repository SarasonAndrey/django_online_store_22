# blog/views.py

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse, reverse_lazy
from .models import BlogPost

# Список статей (только опубликованные)
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Возвращаем только опубликованные статьи
        return BlogPost.objects.filter(is_published=True)

# Детали статьи (увеличение просмотров)
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        # Получаем объект (статью)
        obj = super().get_object(queryset=queryset)

        # Увеличиваем счётчик просмотров на 1 и сохраняем
        obj.views_count += 1
        obj.save()

        return obj

# Создание статьи
class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:list')

# Редактирование статьи (перенаправление после сохранения)
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        return reverse_lazy('blog:detail', args=[str(self.object.pk)])

# Удаление статьи
class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
