from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

class Post(models.Model):
    '''
    Модель поста для блога
    '''

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(verbose_name='Название поста', max_length=255)
    slug = models.SlugField(verbose_name='URL', blank=True, unique=True)
    description = models.TextField(verbose_name='Краткое описание', max_length=500)
    text = models.TextField(verbose_name='Основной текст поста')
    image = models.ImageField(
        verbose_name='Изображение поста',
        blank=True,
        upload_to='images/posts_images',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    status = models.CharField(verbose_name='Статус поста',
                              choices=STATUS_OPTIONS,
                              default='published',
                              max_length=10)
    create = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    author = models.ForeignKey(verbose_name='Автор поста',
                               to=User,
                               on_delete=models.SET_DEFAULT,
                               related_name='author_posts',
                               default=1)
    updater = models.ForeignKey(verbose_name='Обновил',
                                to=User,
                                on_delete=models.SET_NULL,
                                related_name='updater_posts',
                                blank=True,
                                null=True)
    fixed = models.BooleanField(verbose_name='Закреплено', default=False)

    class Meta:
        db_table = 'blog_post'
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=['-fixed', '-create', 'status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Category(MPTTModel):
    '''
    Модель древовидных категорий для постов
    '''

    title = models.CharField(verbose_name='Название категории', max_length=50)
    slug = models.SlugField(verbose_name='URL', blank=True)
    description = models.CharField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(verbose_name='Родительская категория',
                            to='self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            db_index=True,
                            related_name='children'
                            )

    class MPTTMeta:
        '''
        Сортировка по вложенности
        '''

        order_insertion_by = ('title',)

    class Meta:
        '''
        Сортировка, название в админ панели, таблица с данными
        '''

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def __str__(self):
        return self.title