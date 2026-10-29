from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class UserEditForm(forms.ModelForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class PostForm(forms.ModelForm):
    """Форма создания/редактирования публикации."""

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'image',
            'pub_date',
            'location',
            'category',
        )
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'}),
            'text': forms.Textarea(attrs={'rows': 5}),
        }


class CommentCreateForm(forms.ModelForm):
    """Форма добавления комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите ваш комментарий...'}),
        }
