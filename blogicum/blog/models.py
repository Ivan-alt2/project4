from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimestampModel(models.Model):
    """Базовая модель с полями публикации и времени создания."""

    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Category(TimestampModel):
    """Категория для публикаций."""

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=64,
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(TimestampModel):
    """Местоположение публикации."""

    name = models.CharField(
        verbose_name='Название места',
        max_length=256,
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(TimestampModel):
    """Публикация (пост) в блоге."""

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts_images',
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return self.title


class Comment(TimestampModel):
    """Комментарий к публикации."""

    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментируемый пост',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        # Здесь оставляем составную строку — она не обрезается, и это нормально
        return f'Комментарий {self.author.username} поста {self.post.title}'
