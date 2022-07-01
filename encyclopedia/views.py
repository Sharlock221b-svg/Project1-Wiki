from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.urls import reverse
import markdown2
from . import util
from django import forms
import random

#Form to create a new Page
class newEntryPage(forms.Form):
    title = forms.CharField(
        label="Title", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    text = forms.CharField(
        label="Conent", widget=forms.Textarea(attrs={"class": "form-control"})
    )

#Form for editing a page
class editEntry(forms.Form):
    text = forms.CharField(
        label="Conent", widget=forms.Textarea(attrs={"class": "form-control"})
    )


# defining index function
def index(request):
    # if accessed the POST request
    if request.method == "POST":
        # accessing froms data and list of entries
        title = request.POST.get("q")
        res = util.get_entry(title)

        # If item found then get render its page
        if res != None:
            return render(
                request,
                "encyclopedia/page.html",
                {"title": title.capitalize(), "body": markdown2.markdown(res)},
            )

        # else if not then look through the list for substring and then render search.html
        else:
            entries = util.list_entries()
            match_entries = []

            for entry in entries:
                if title.lower() in entry.lower():
                    match_entries.append(entry)

            return render(
                request,
                "encyclopedia/search.html",
                {"title": title, "entries": match_entries},
            )
    # else if accessed via get then render all the entries
    else:
        return render(
            request,
            "encyclopedia/index.html",
            {"entries": util.list_entries()},  # returns the list of entires
        )


def getPage(request, title):
    page = util.get_entry(title)
    # if the entry don't exists then renders the Not Found Page
    if page is None:
        return render(
            request,
            "encyclopedia/page.html",
            {
                "title": title.capitalize(),
                "body": f"<h2 style='color: #86AAFF; margin-left: 40px; margin-top: 20px;'><i>{title}</i> not found</h2>",
            },
        )
    # Else renders the page as an HTML file
    else:
        return render(
            request,
            "encyclopedia/page.html",
            {"title": title.capitalize(), "body": markdown2.markdown(page)},
        )


#newPage function
def newPage(request):
    #if accessed via POST
    if request.method == "POST":
        #Gets tha form
        form = newEntryPage(request.POST)

        if form.is_valid():#Checks for validity

            title = form.cleaned_data["title"]
            content = form.cleaned_data["text"]
            exits = util.get_entry(title)

            if exits is None:
                #Save the entry and gets the page via getPage 
                util.save_entry(title, content)
                return HttpResponseRedirect(
                    reverse("encyclopedia:getPage", args=(title,))
                )
            else:   #If such form already exits
                return render(
                    request,
                    "encyclopedia/page.html",
                    {
                        "title": "Already Exists",
                        "body": f"<h2 style='color: #86AAFF; margin-left: 40px; margin-top: 20px;'><i>{title}</i> Already Exists </h2>",
                    },
                )

        else:
            return HttpResponse("Please Fill the Form Correctly!!.. Retry")
   
   #Renders a form to create a new page
    else:
        return render(request, "encyclopedia/newPage.html", {"form": newEntryPage()})


def edit(request, title):
    if request.method == "POST":
        #If accessed via post then gets the changed content and save it
        form = editEntry(request.POST)

        if form.is_valid():
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("encyclopedia:getPage", args=(title,)))
        else:
            return HttpResponse("Please Fill the Form Correctly!!.. Retry")

    else:
        #Gets the content of the page woth get_entry function and title, then initialize the form with the value received and renders the form with the content.
        data = util.get_entry(title)
        dic = {"text": data}
        form = editEntry(initial=dic)
        return render(
            request,
            "encyclopedia/editEntry.html",
            {"title": title.capitalize(), "form": form},
        )


def Random(request):
    #Gets the list of entries selects one at random and then displays it
    arr = util.list_entries()
    title = random.choice(arr)
    return HttpResponseRedirect(reverse("encyclopedia:getPage", args=(title,)))
