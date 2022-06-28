from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import markdown2
from . import util

#defining index function renders all the entries to the page
def index(request):
    if request == "POST":
        print(request)
    else:
      return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()#returns the list of entires
    })


def getPage(request, title):
    page = util.get_entry(title)
    #if the entry don't exists then renders the Not Found Page
    if page is None: 
        return render(request, "encyclopedia/page.html", {
            "title": title.capitalize(),
            "body": f"<h2 style='color: #86AAFF; margin-left: 40px; margin-top: 20px;'><i>{title}</i> not found</h2>"
        })
    #Else renders the page as an HTML file
    else:
        #print(page)
        return render(request, "encyclopedia/page.html", {
            "title": title.capitalize(),
            "body": markdown2.markdown(page)
        })

