from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, "pages/about.html")

def contact(request):
    return render(request, "pages/contact.html")

def faq(request):
    return render(request, "pages/faq.html")

def team(request):
    return render(request, "pages/team.html")