from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from news.models import Article


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ('title', 'publication_date')
    list_display_links = ('title', )