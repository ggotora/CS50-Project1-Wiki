import re
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from encyclopedia.forms import NewEntryForm
import markdown2 
import random

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
        'entry': entry, 
        'title': title
    })

def error404(request, exception='Page not found'):
    return render(request,'404.html')

def search(request):
    query = request.GET.get('q')
    results = []
   
    if util.get_entry(query):
        return render(request, "encyclopedia/entry.html", {
            'entry': markdown2.markdown(util.get_entry(query))
            })
    else:
        for title in util.list_entries():
            print(title.lower().find(query.lower()) == -1)
            if title.lower().find(query.lower()) != -1:
                results.append(title)
        return render(request, "encyclopedia/results.html", {
        "results": results, 
        'query': query
    })


def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            editable = form.cleaned_data['editable']
            if editable or title not in util.list_entries():
                util.save_entry(title, content)
                return HttpResponseRedirect(f'/wiki/{title}')           
            elif title in util.list_entries():
                return render(request, "encyclopedia/duplicate_entry.html" , {
                    'duplicate': util.get_entry(title), 
                    'duplicate_title': title, 
                    'entries': util.list_entries()
                })
                
    else:
        form = NewEntryForm()
        return render(request, 'encyclopedia/new_entry.html', {
            'form': form
        })

def edit_entry(request, title):
    data = {
        'title': title,
        'content': util.get_entry(title), 
        'editable': True
    }
    form = NewEntryForm(data)
    util.save_entry(data['title'], data['content'])
    return render(request, 'encyclopedia/new_entry.html', {
            'form': form
        })
def random_page(request):
    random_int = (random.randint(0, len(util.list_entries())) -1 )
    print(len(util.list_entries()))
    title = util.list_entries()[random_int]
    return HttpResponseRedirect(f'/wiki/{title}')