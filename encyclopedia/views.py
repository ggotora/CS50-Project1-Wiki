import re
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
        entry = markdown2.markdown(util.get_entry(title))
    except:
        raise Http404('Page not found')
    return render(request, 'encyclopedia/entry.html', {
        'entry': entry
    })

def error404(request, exception='Page not found'):
    return render(request,'404.html')