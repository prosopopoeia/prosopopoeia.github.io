from django.shortcuts import render, redirect
import random
from markdown2 import Markdown
from . import util
from encyclopedia.forms import AddPageForm

def search_entries(search_term):
    all_entries = util.list_entries()
    matching_entries = []
    for entry in all_entries:
        if search_term in entry:
            matching_entries.append(entry)
    return matching_entries
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def newpage(request):    
    if request.method == "POST":
        vapform = AddPageForm(request.POST)
        
        if vapform.is_valid():
            vtitle = vapform.cleaned_data["title"]
            vbody = vapform.cleaned_data["body"]
            #TBD FIX BELOW TO SIMPLY OFFER UP THE FORM AGAIN
            if util.get_entry(vtitle) is not None:
                return render(request, "encyclopedia/addpage.html", {
                "dtitle" : vtitle,
                #"label"  : "Entry",
                "dbody" : "error: entry already exists!",  
                "msg" : "back"
               })

            util.save_entry(vtitle, vbody)
            return render(request, "encyclopedia/displaypage.html", {
                "dtitle" : vtitle,
                "label"  : "Entry",
                "dbody" : vbody,            
               })            
            
    return render(request, "encyclopedia/addpage.html", {
        "tapform" : AddPageForm(),
        "msg" : "save"
    })
    
def entrypage(request, utitle = None):    
    if request.method == "POST":
        utitle = request.POST.get('q')
        wiki_entry = util.get_entry(utitle)
        if wiki_entry is None:
            possible_entries = search_entries(utitle)
            return render(request, 'encyclopedia/index.html', {
                "entries" : possible_entries
            })
            
    wiki_entry = util.get_entry(utitle)
    if wiki_entry is not None:
        vbody = wiki_entry
    else:
        return render(request, 'encyclopedia/error.html', { "dtitle" : utitle})
     
    marker = Markdown() 
    return render(request, "encyclopedia/displaypage.html", {
        "dtitle" : utitle,
        "label"  : "Entry",
        "dbody"  : marker.convert(vbody),
        "msg"    : "edit"
    })
    
def editpage(request, utitle = None):    
    wiki_entry = util.get_entry(utitle)
    vapform = AddPageForm({"title" : utitle, "body" : wiki_entry})
    if vapform.is_valid():
        vtitle = vapform.cleaned_data["title"]
        #vbody = vapform.cleaned_data["body"]
            
    return render(request, "encyclopedia/editpage.html", {
        "dtitle" : utitle,
        "label"  : "Edit",
        "tapform": vapform,
        "msg"    : "Save Edit"
        
    })

def saveeditpage(request):       
    vtitle = request.POST.get('title')
    vbody = request.POST.get('body')
    util.save_entry(vtitle, vbody)
    
    return render(request, "encyclopedia/displaypage.html", {
        "dtitle" : vtitle,
        "label"  : "Edit",
        #"tapform": vapform,
        "msg"    : "Edit"        
    })  
    
def randompage(request):
    all_entries = util.list_entries()
    randomIndex = random.randint(0, len(all_entries))
    wiki_entry = util.get_entry(all_entries[randomIndex])
    
    return render(request, "encyclopedia/displaypage.html", {
        "dtitle" : all_entries[randomIndex],
        "label"  : "Entry",
        "dbody"  : wiki_entry,
        "msg"    : "edit"
    })