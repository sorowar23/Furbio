from django.shortcuts import render, get_object_or_404,redirect

from orders.models import OrderProduct
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Count
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
# Create your views here.
def store(request, category_slug=None):
     categories = None
     products = None

     if category_slug!= None:
          categories = get_object_or_404(Category, slug=category_slug)
          products = Product.objects.filter(category=categories)
          filtered_products = products.filter(is_available=True)
          paginator = Paginator(filtered_products, 2)
          page = request.GET.get('page')
          paged_products = paginator.get_page(page)
          product_count = filtered_products.count()
          product_count_by_categories = Category.objects.annotate(product_count=Count("products"))
     else:
          products = Product.objects.all()
          filtered_products = products.filter(is_available=True).order_by('id')
          paginator = Paginator(filtered_products, 3)
          page = request.GET.get('page')
          paged_products = paginator.get_page(page)
          product_count = filtered_products.count()
          product_count_by_categories = Category.objects.annotate(product_count=Count("products"))

     context = {
          'products': paged_products,
          'product_count': product_count,
          'categories': categories,
          'product_count_by_categories': product_count_by_categories,
     }
     return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
     try:
          single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
          in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
          related_products = single_product.get_related_products()
         
     except Exception as e:
          raise e
     
     if request.user.is_authenticated:
          try:
               orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
          except: 
               orderproduct.DoesNotExist
               orderproduct = None
     else:
          orderproduct = None

     reviews = ReviewRating.objects.filter(product_id =single_product.id, status=True)
     
     context = {
          'single_product': single_product,
          'in_cart': in_cart,
          'related_products': related_products,
          'orderproduct': orderproduct,
          'reviews':reviews,
     }

     return render(request, 'store/product_detail.html', context)

def search(request):
     if 'keyword' in request.GET:
          keyword = request.GET['keyword']
          if keyword:
               products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
               product_count = products.count()
               product_count_by_categories = Category.objects.annotate(product_count=Count("products"))
          else:
               products = [] 
               product_count = 0
               product_count_by_categories = []
               
     context = {
          'products': products,
          'product_count': product_count,
          'product_count_by_categories': product_count_by_categories,

     }
     return render(request, 'store/store.html', context)
     

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')+'?tab=reviews';
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
                #return redirect(f'/product/{product_id}/?tab=reviews')
            
               