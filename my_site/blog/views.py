from django.shortcuts import render
from datetime import date

# Create your views here.

posts = [
  {
    "slug": "devops-culture",
    "image": "DevOps-lifecycle.png",
    "author": "s403o",
    "date": date(2023, 2, 24),
    "title": "DevOps",
    "excerpt": "DevOps is the combination of cultural philosophies, practices, and tools that increases an organization's ability to deliver applications and services at high velocity.",
    "content": """
    DevOps is the combination of cultural philosophies, practices, and tools that increases an organizations ability to deliver applications and services at high velocity: evolving and improving products at a faster pace than organizations using traditional software development and infrastructure management processes. This speed enables organizations to better serve their customers and compete more effectively in the market.
  """
  },

  {
    "slug": "devops-roadmap",
    "image": "devops-roadmap.png",
    "author": "s403o",
    "date": date(2023, 2, 24),
    "title": "DevOps",
    "excerpt": "DevOps is the combination of cultural philosophies, practices, and tools that increases an organization's ability to deliver applications and services at high velocity.",
    "content": """
    DevOps is the combination of cultural philosophies, practices, and tools that increases an organizations ability to deliver applications and services at high velocity: evolving and improving products at a faster pace than organizations using traditional software development and infrastructure management processes. This speed enables organizations to better serve their customers and compete more effectively in the market.
  """
  },

  {
    "slug": "Site-Reliability-Engineering",
    "image": "devops-roadmap.png",
    "author": "s403o",
    "date": date(2023, 2, 24),
    "title": "SRE",
    "excerpt": "SRE is what you get when you treat operations as if it’s a software problem.",
    "content": """
    SRE is what you get when you treat operations as if it’s a software problem. Our mission is to protect, provide for, and progress the software and systems behind all of Google’s public services — Google Search, Ads, Gmail, Android, YouTube, and App Engine, to name just a few — with an ever-watchful eye on their availability, latency, performance, and capacity.
  """
  },
]


def starting_page(request):
    
    return render(request, "blog/index.html")


def posts(request):
    return render(request, "blog/all-posts.html")


def post_details(request, slug):  # slug (dynamic segment)
    return render(request, "blog/post-details.html")
