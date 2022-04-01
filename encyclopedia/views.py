import re
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from encyclopedia.forms import NewEntryForm
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
