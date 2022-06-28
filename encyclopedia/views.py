from turtle import title
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import markdown2
from . import util

#defining index function 
def index(request):
    #if accessed the POST request
    if request.method == 'POST':
        #accessing froms data and list of entries
        title = request.POST.get('q')
        res = util.get_entry(title)

        #If item found then get render its page
        if res != None:
           return render(request, "encyclopedia/page.html", {
            "title": title.capitalize(),
            "body": markdown2.markdown(res)
           })

        #else if not then look through the list for substring and then render search.html
        else:
          entries = util.list_entries()
          match_entries = []

          for entry in entries:
              if title.lower() in entry.lower():
                  match_entries.append(entry)

          return render(request, "encyclopedia/search.html", {
            "title": title,
            "entries": match_entries
          })
    #else if accessed via get then render all the entries
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


