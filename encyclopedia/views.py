from django.http import Http404
from django.shortcuts import render
import markdown2 

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    try:
        entry = util.get_entry(title)
    except:
        raise Http404('Page Not Found!!')
    return render(request, "encyclopedia/entry.html", {
        'entry': markdown2.markdown(entry)
    })