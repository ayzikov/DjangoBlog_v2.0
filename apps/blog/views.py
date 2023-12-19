from django.shortcuts import render
from django.views.generic import ListView, DetailView


from .models import Post, Category

class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Главная страница'
        return context


class PostDetailView(DetailView):
    '''
    В класс передается slug из url и с помощью него ищется подходящий объект модели model
    '''
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        '''
        Функция передает словарь, который в последующем можно использовать в шаблонах
        '''
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = self.object.title
        return context


class PostFromCategory(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    category = None

    def get_queryset(self):
        '''
        Функция возвращает queryset с постами с выбранной категорией
        '''

        # получем из url slug категории
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        # получаем посты с данной категорией
        queryset = Post.objects.filter(category__slug=self.category.slug)
        # если в данной категории постов нет, то ищем посты во всех дочерних категориях данной категории
        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Post.objects.filter(category__in=sub_cat)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = self.category.title
        return context

