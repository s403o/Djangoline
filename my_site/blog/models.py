from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class Tag(models.Model):
    captions = models.CharField(max_length=20)

    def __str__(self):
        return self.captions
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name()
class Post(models.Model):
    title = models.CharField(max_length=100)
    image_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    content = models.TextField(validators=[MinValueValidator("10")])
    slug = models.SlugField(unique=True) # db_index=True auto set
    excerpt = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField(Tag)
    