from django.urls import path
from . import views


urlpatterns = [
  path("", views.starting_page, name="starting_page"),
  path("posts", views.posts, name="posts"),
  path("posts/<slug:slug>", views.post_details, name="post_details"), # /posts/post_title (slug transformer)
]
