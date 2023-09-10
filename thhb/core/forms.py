from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'subtitle', 'author', 'pub_date', 'category', 'image', 'image_alt', 'content')
        prepopulated_fields = {'slug': ('title',)}
      #  exclude = ['published_date']