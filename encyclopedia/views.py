from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

def convert_md_html(title):
    entry=util.get_entry(title)
    markdowner = Markdown()
    if entry == None:
        return None
    html = markdowner.convert(entry)
    return html

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html=convert_md_html(title)
    if html == None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content" : html
    })

def search(request):
    keyword=request.GET.get("q")
    entries=util.list_entries()
    #If exact match:
    if keyword in entries:#loop through list-exact match among list items
        return HttpResponseRedirect(reverse("entry", args=[keyword]))
    #No exact match(look for substrings):
    results=[]
    for entry in entries:
        if keyword.lower() in entry.lower(): #loop through string - partial match inside that string
            results.append(entry)
    return render(request, "encyclopedia/search.html", {"entries": results})

def new_page(request):
  if request.method=="POST":
    title= request.POST.get("title")
    content=request.POST.get("content")
    entries=util.list_entries()
    if title in entries:
      return render(request, "encyclopedia/error.html", {
            "message": "This title already exists."})
    util.save_entry(title, content)
    return HttpResponseRedirect(reverse("entry", args=[title]))
  #for get requests show the add page form
  return render(request, "encyclopedia/new_page.html")

def edit(request, title):
    if request.method =="POST":
        content=request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    content=util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content})

def random_page(request):
    random_title=random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", args=[random_title]))
