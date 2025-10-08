from django.shortcuts import render
from store.models import Product
from django.db.models import Count
from store.models import Category

def home(request):
    products = Product.objects.all()
    filtered_products = products.filter(is_available=True)
    # Featured products
    featured_products = Product.objects.filter(is_featured=True, is_available=True)
    # Hot sale products
    hot_sale_products = Product.objects.filter(is_hot_sale=True, is_available=True)
    product_count_by_categories = Category.objects.annotate(product_count=Count("products"))
    
    context = {
        'products': filtered_products,
        'product_count_by_categories': product_count_by_categories,
        'featured_products': featured_products,
        'hot_sale_products': hot_sale_products,
       
    }
    return render(request,'home.html', context)


def about(request):
    return render(request, "about.html")