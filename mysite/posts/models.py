from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default='')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=60)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Topics'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Posts'

    def __str__(self):
        words = (self.text or "").split()
        head = " ".join(words[:5])
        return head + ("..." if len(words) > 5 else "")
