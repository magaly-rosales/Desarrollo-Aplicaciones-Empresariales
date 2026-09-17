from django.contrib import admin

# Register your models here.
from .models import Author, AuthorProfile, Book, Category, Publisher, Publication


class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 1


class AuthorProfileInline(admin.StackedInline):
    model = AuthorProfile


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [AuthorProfileInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [PublicationInline]
    filter_horizontal = ['categories']


admin.site.register(Category)
admin.site.register(Publisher)
admin.site.register(Publication)