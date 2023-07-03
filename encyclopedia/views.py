#Import all the dependencies
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from . import util
import random

#Helper function
#Helper function to ready a page content that is to be stored
def create_page(title, content):
    return "# " + title + "\n\n" + content


#Lists all the entries currently stored.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


"""Takes input from the url and searches for an entry with the name.
If no entry is found, Not Found message is displayed otherwise, the
entry is converted from markdown to HTML and rendered on entry template."""
def entrypage(request, title):
    entry_md = util.get_entry(title)
    if entry_md is None:
        return render(request, "encyclopedia/notfound.html")
    html = markdown2.markdown(entry_md)
    return render(request, "encyclopedia/entry.html", {
        "title": title, "entry": html
    })


"""Gets the data from the input field and tries to find the 
a matching result among the stored entries. If found, it renders the entry page
If not found, creates a list of possible results by checking
if the input is a sub-string of the entry string."""
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


"""Takes in the user inputted title and content. Checks if an entry
with the same title already exists. If it does, then return an appropriate
error. Otherwise, takes the title and content to create a new entry and then
render the entry"""
def add(request):
        if request.method == "POST":
            title = request.POST["title"]
            entry = util.get_entry(title)            
            if entry is not None:
                return render(request, "encyclopedia/error.html")
            body = request.POST["content"]
            content = create_page(title, body)
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}/")
        return render(request, "encyclopedia/newpage.html")


"""Lets the user edit the information in a page and stores the edited
information."""
def edit(request, title):
    if request.method == "POST":
        update = request.POST["content"]        
        util.save_entry(title, update)
        return HttpResponseRedirect(f"/wiki/{title}/")
    precontent = util.get_entry(title)
    return render(request, "encyclopedia/editpage.html", {
        "title": title, "precontent" : precontent
    })


"""Selects a page randomly by generating an integer between 0 and the number of
entries stored. The integer is then used as an index to access the title at
that index position. Then that title is rendered using the entrypage view."""
def randompage(request):
    entries = util.list_entries()
    entry = random.randint(0, len(entries)-1)
    page = entries[entry]
    return entrypage(request, page)
