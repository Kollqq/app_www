from django.contrib import admin
from unicodedata import category

from .models import Category, Topic, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created')
    list_filter = ('category', 'name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'topic_with_category', 'text_preview', 'created_at', 'updated_at', 'created_by')
    list_filter = ('topic', 'topic__category', 'created_by', 'topic__name', 'topic__category__name')

    @admin.display(description='Topic', ordering='topic__name')
    def topic_with_category(self, obj):
        return f"{obj.topic.name} ({obj.topic.category.name})"

    def text_preview(self, obj):
        words = (obj.text or "").split()
        head = " ".join(words[:5])
        return head + ("..." if len(words) > 5 else "")
    text_preview.short_description = 'Tekst (5 słów)'
    text_preview.admin_order_field = 'text'