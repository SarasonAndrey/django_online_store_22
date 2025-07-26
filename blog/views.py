# blog/views.py

from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import BlogPost


class BlogPostListView(ListView):
    """Отображает список опубликованных статей."""

    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Возвращает только опубликованные статьи."""
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Отображает детали статьи и увеличивает счётчик просмотров."""

    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Получает объект и увеличивает количество просмотров."""
        obj = super().get_object(queryset=queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogPostCreateView(CreateView):
    """Форма для создания новой статьи."""

    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:list")


class BlogPostUpdateView(UpdateView):
    """Форма для редактирования статьи."""

    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ["title", "content", "preview", "is_published"]

    def get_success_url(self):
        """Перенаправляет на страницу статьи после редактирования."""
        return reverse_lazy("blog:detail", args=[str(self.object.pk)])


class BlogPostDeleteView(DeleteView):
    """Подтверждение и удаление статьи."""

    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:list")
