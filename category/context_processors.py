from .models import Category
from django.db.models import Count

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

