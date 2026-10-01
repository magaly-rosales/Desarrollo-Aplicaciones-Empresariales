from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Genre, Movie


def genre_recommendations(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = (
        Movie.objects.filter(genres=genre)
        .annotate(avg_rating=Avg('ratings__score'))
        .order_by('-avg_rating')
    )
    return render(request, 'movies/genre_recommendations.html', {
        'genre': genre,
        'movies': movies,
    })


def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'movies/genre_list.html', {'genres': genres})