from django.shortcuts import render
from datetime import date

# Create your views here.

all_posts = [
  {
      "slug": "devops-culture",
      "image": "DevOps-lifecycle.png",
      "author": "s403o",
      "date": date(2023, 2, 23),
      "title": "DevOps Culture",
      "excerpt": "DevOps is the combination of cultural philosophies, practices, and tools that increases an organization's ability to deliver applications and services at high velocity.",
      "content": """
  DevOps is the combination of cultural philosophies, practices, and tools that increases an organizations ability to deliver applications and services at high velocity: evolving and improving products at a faster pace than organizations using traditional software development and infrastructure management processes. This speed enables organizations to better serve their customers and compete more effectively in the market.
"""
  },

  {
      "slug": "devops-roadmap",
      "image": "devops-roadmap.png",
      "author": "s403o",
      "date": date(2023, 2, 22),
      "title": "DevOps Roadmap",
      "excerpt": "DevOps is the combination of cultural philosophies, practices, and tools that increases an organization's ability to deliver applications and services at high velocity.",
      "content": """
  DevOps is the combination of cultural philosophies, practices, and tools that increases an organizations ability to deliver applications and services at high velocity: evolving and improving products at a faster pace than organizations using traditional software development and infrastructure management processes. This speed enables organizations to better serve their customers and compete more effectively in the market.
"""
  },

  {
      "slug": "Site-Reliability-Engineering",
      "image": "sre.png",
      "author": "s403o",
      "date": date(2023, 2, 24),
      "title": "SRE",
      "excerpt": "SRE is what you get when you treat operations as if it’s a software problem.",
      "content": """
  SRE is what you get when you treat operations as if it’s a software problem. Our mission is to protect, provide for, and progress the software and systems behind all of Google’s public services — Google Search, Ads, Gmail, Android, YouTube, and App Engine, to name just a few — with an ever-watchful eye on their availability, latency, performance, and capacity.
"""
  },
]


def get_date(post):
  return post['date']


def starting_page(request):
  # sorted_posts = all_posts.sort(key=get_date) # sort existing list
  sorted_posts = sorted(all_posts, key=get_date) # sort to new list
  latest_posts = sorted_posts[-3:]
  return render(request, "blog/index.html", {
    "posts": latest_posts,
  })


def posts(request):
  return render(request, "blog/all-posts.html")


def post_details(request, slug):  # slug (dynamic segment)
  return render(request, "blog/post-details.html")
