from django.db import models
from django.template.defaultfilters import slugify

from tinymce.models import HTMLField
import datetime


class BlogPost(models.Model):

    class CategoryType(models.TextChoices):
        MAIN = 'MN', 'Main'
        RELATED = 'RL', 'Related'
        OTHER = 'OT', 'Other'

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, null=False, unique=True)
    subtitle = models.CharField(max_length=250)
    author = models.CharField(max_length=50, default="Nicholas Thorne")
    image = models.ImageField(upload_to='static/img/', null=False, blank=False)
    image_alt = models.CharField(max_length=100)
    pub_date = models.DateField(default=datetime.date.today)
    last_updated = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=2,
                                choices=CategoryType.choices,
                                default=CategoryType.MAIN)

    content = HTMLField()

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:single_post", kwargs={"slug": self.slug})

    # Auto-generate slug from title when saving
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


