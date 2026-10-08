from django.contrib import admin

from .models import Article, Author, Category

admin.site.site_header = 'Administración del Portal de Noticias'
admin.site.site_title = 'Portal de Noticias'
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at')
    list_filter = ('published_at', 'author', 'categories')
    search_fields = ('title', 'summary', 'body')
    date_hierarchy = 'published_at'