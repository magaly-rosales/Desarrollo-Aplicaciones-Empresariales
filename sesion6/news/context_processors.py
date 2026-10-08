from django.db.models import Count

from .models import Category


def sidebar_categories(request):
    categories = Category.objects.annotate(total=Count('articles'))
    return {'sidebar_categories': categories}