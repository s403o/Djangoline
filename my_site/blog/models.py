from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()
class Post(models.Model):
    title = models.CharField(max_length=100)
    image_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    content = models.TextField(validators=[MinValueValidator(10)])
    slug = models.SlugField(unique=True) # db_index=True auto set
    excerpt = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name="posts")
    