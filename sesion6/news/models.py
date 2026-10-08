from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']
    def __str__(self):
        return self.name
    
    
class Author(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
    
    
class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    body = models.TextField()
    featured_image = models.ImageField(upload_to='articles/')
    published_at = models.DateTimeField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='articles')
    categories = models.ManyToManyField(Category, related_name='articles')
    class Meta:
        ordering = ['-published_at']
    def __str__(self):
        return self.title