from django.shortcuts import render
from store.models import Product

def home(request):
    products = Product.objects.all()
    filtered_products = products.filter(is_available=True)
    
    context = {
        'products': filtered_products,
    }
    return render(request,'home.html', context)