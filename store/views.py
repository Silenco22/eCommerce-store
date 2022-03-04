from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_all(request):
    #display all the products on home page not optimized query
    # products = Product.objects.all()
    #optimized query: prefetch_related("product_image").filter(is_active=True) 
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    return render(request, 'store/index.html', {'products': products})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    #get all the products form the category and all of his descendants ##django mtpp tool allows us to use get_descendants
    products = Product.objects.filter(category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True))
    return render(request, 'store/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/single.html', {'product': product})
