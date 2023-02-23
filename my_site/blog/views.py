from django.shortcuts import render

# Create your views here.

def starting_page(request):
  return render(request, "blog/index.html")

def posts(request):
  return render(request, "blog/all-posts.html")

def post_details(request, slug): # slug (dynamic segment)
  return render(request, "blog/post-details.html")