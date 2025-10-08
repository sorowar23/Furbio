from django.db import models
from accounts.models import Account
from category.models import Category
from django.urls import reverse
from django.db.models import Avg,Count
from django_ckeditor_5.fields import CKEditor5Field  
# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug         = models.SlugField(max_length=200, unique=True)
    description  = models.TextField(max_length=500, blank=True)
    full_description = CKEditor5Field('Description', config_name='default', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Leave blank if product is not on sale"
    )
    images   = models.ImageField(upload_to='photos/products')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    is_featured = models.BooleanField(default=False)   # Featured Product
    is_hot_sale = models.BooleanField(default=False)

    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def get_display_price(self):
        """Return sale price if available, otherwise regular price."""
        return self.sale_price if self.sale_price else self.price
    
    def get_related_products(self):
        """Return products from the same category, excluding this one."""
        return Product.objects.filter(
            category=self.category
        ).exclude(id=self.id)[:5]  # Limit to 5

    def averageReview(self):
         reviews = ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
         avg = 0
         if reviews['average'] is not None:
              avg = float(reviews['average'])
              return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

         
    def __str__(self):
        return self.product_name
    

class VariationManager(models.Manager):
     def colors(self):
          return super(VariationManager, self).filter(variation_category='color', is_active=True)
     
     def sizes(self):
          return super(VariationManager, self).filter(variation_category='size', is_active=True)
     
     def weight(self):
          return super(VariationManager, self).filter(variation_category='weight', is_active=True)
    
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
    ('weight', 'weight'),
)

class Variation(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        variation_category = models.CharField(max_length=100, choices=variation_category_choice)
        variation_value    = models.CharField(max_length=100)
        is_active          = models.BooleanField(default=True)
        created_date       = models.DateTimeField(auto_now=True)

        objects = VariationManager()

        def __str__(self):
             return self.variation_value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    gallery_image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.product_name}"
    

class ReviewRating(models.Model):
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     user = models.ForeignKey(Account, on_delete=models.CASCADE)
     subject = models.CharField(max_length=100, blank=True)
     review = models.TextField(max_length=100,blank=True)
     rating = models.FloatField()
     ip = models.CharField(max_length=20,blank=True)
     status = models.BooleanField(default=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
          return self.subject