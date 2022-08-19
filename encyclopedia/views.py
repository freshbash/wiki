from django.shortcuts import render

from django.http import HttpResponseRedirect

from django.urls import reverse

import markdown2

from . import util

import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entrypage(request, title):
    entry_md = util.get_entry(title)
    if entry_md is None:
        return render(request, "encyclopedia/notfound.html")
    html = markdown2.markdown(entry_md)
    return render(request, "encyclopedia/entry.html", {
        "title": title, "entry": html
    })

def results(request):
    entries = util.list_entries()
    possible_entries = []
    q = request.GET['q']
    for entry in entries:
        if q.lower() == entry.lower():
            return entrypage(request, entry)
        if q.lower() in entry.lower():
            possible_entries.append(entry)
    return render(request, "encyclopedia/results.html", {
        "possible": possible_entries
    })

def add(request):
        if request.method == "POST":
            title = request.POST["title"]
            entries = util.list_entries()
            for entry in entries:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/error.html")
            content = request.POST["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}/")
        return render(request, "encyclopedia/newpage.html")

def edit(request, title):
    if request.method == "POST":
        update = request.POST["content"]
        util.save_entry(title, update)
        return HttpResponseRedirect(f"/wiki/{title}/")
    precontent = util.get_entry(title)
    return render(request, "encyclopedia/editpage.html", {
        "title": title, "precontent" : precontent
    })

def randompage(request):
    entries = util.list_entries()
    entry = random.randint(0, len(entries)-1)
    page = entries[entry]
    return entrypage(request, page)
