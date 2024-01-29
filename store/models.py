from django.db import models
from django.urls import reverse
from category2.models  import Category

# Create your models here.
class Product(models.Model):
    product_name        = models.CharField(max_length  = 50, unique = True)
    slug                = models.SlugField(max_length = 50, unique = True )
    description         = models.TextField(max_length = 250, unique = True) 
    price               = models.IntegerField()
    image               = models.ImageField()
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default = True)
    category            = models.ForeignKey(Category, on_delete = models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add = True)
    modified_date       = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_page', args=[self.category.slug, self.slug])    