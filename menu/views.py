from django.shortcuts import render, redirect
from .models import Product, Logo, Feedback, category, ProductClick
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
import time


# def index(request):
#     logo = Logo.objects.last()
#     cat = category.objects.all()
#     return render(request, 'index.html', {'cat': cat, 'logo':logo })

def index(request):
    logo = Logo.objects.last()
    categories = category.objects.all()
    first_category = categories.first()  # İlk kategoriyi al
    products = Product.objects.filter(category=first_category)  # İlk kategoriye ait ürünleri al

    context = {
        'categories': categories,
        'products': products,
        'logo': logo
    }
    return render(request, 'index.html', context)

def category_products(request, category_id):
    logo = Logo.objects.last()
    categories = category.objects.all()
    selected_category = get_object_or_404(category, id=category_id)
    products = Product.objects.filter(category=selected_category)
    return render(request, 'index.html', {'categories': categories, 'products': products, 'selected_category': selected_category, 'logo': logo})

def urun(request):
    products = Product.objects.all()
    logo = Logo.objects.last()
    return render(request, 'urun.html', {'products': products,'logo': logo})

def track_click(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    ProductClick.objects.create(product=product)
    return JsonResponse({'status': 'success'})

# def category_products(request, category_id):
#     category_obj = get_object_or_404(category, pk=category_id)
#     products = Product.objects.filter(category=category_obj)
#     logo = Logo.objects.last()
#     if request.method == 'POST':
#         product.click_count += 1
#         product.save()
#     return render(request, 'urun.html', {'products': products, 'logo': logo})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    logo = Logo.objects.last()
    if request.method == 'POST':
        product.click_count += 1
        product.save()
    return render(request, 'urundetay.html', {'product': product, 'logo': logo})


# def product_detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     logo = Logo.objects.last()
#     return render(request, 'urundetay.html', {'product': product,'logo': logo})

def feedback(request):
    logo = Logo.objects.last()
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Feedback.objects.create(name=name, surname=surname, email=email, message=message)
        time.sleep(3)  # 3 saniye bekle
        return redirect('home')  # Ana sayfaya yönlendir
    return render(request, 'feedback.html', {'logo': logo})


def admin_page(request):
    if request.method == 'POST':
        if 'catname' in request.POST:
            catname = request.POST.get('catname')
            catimage = request.FILES.get('catimage')
            if catname and catimage:
                category.objects.create(catname=catname, catimage=catimage)
        elif 'productname' in request.POST:
            name = request.POST.get('productname')
            price = request.POST.get('price')
            image = request.FILES.get('productimage')
            detail = request.POST.get('detail')
            category_id = request.POST.get('category')
            if all([name, price, image, detail, category_id]):
                category_instance = category.objects.get(id=category_id)
                Product.objects.create(name=name, price=price, image=image, detail=detail, category=category_instance)
        return redirect('admin_page')
    
    categories = category.objects.all()
    products = Product.objects.all()
    return render(request, 'admin.html', {'categories': categories, 'products': products})

def increment_click_count(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.click_count += 1
    product.save()
    return redirect('admin_page')

def admin_page(request):
    if request.method == 'POST':
        if 'catname' in request.POST:
            catname = request.POST.get('catname')
            catimage = request.FILES.get('catimage')
            if catname and catimage:
                category.objects.create(catname=catname, catimage=catimage)
        elif 'productname' in request.POST:
            name = request.POST.get('productname')
            price = request.POST.get('price')
            image = request.FILES.get('productimage')
            detail = request.POST.get('detail')
            category_id = request.POST.get('category')
            if all([name, price, image, detail, category_id]):
                category_instance = category.objects.get(id=category_id)
                Product.objects.create(name=name, price=price, image=image, detail=detail, category=category_instance)
        elif 'logoimage' in request.FILES:
            logoimage = request.FILES.get('logoimage')
            if logoimage:
                Logo.objects.create(image=logoimage)
        return redirect('admin_page')
    
    categories = category.objects.all()
    feedbacks = Feedback.objects.all()
    products = Product.objects.all()
    latest_logo = Logo.objects.order_by('-uploaded_at').first()
    return render(request, 'admin.html', {
        'categories': categories,
        'products': products,
        'latest_logo': latest_logo,
        'feedbacks': feedbacks
    })

def edit_category(request, category_id):
    cat = get_object_or_404(category, id=category_id)
    if request.method == 'POST':
        cat.catname = request.POST.get('catname')
        if 'catimage' in request.FILES:
            cat.catimage = request.FILES.get('catimage')
        cat.save()
        return redirect('admin_page')
    return render(request, 'edit_category.html', {'category': cat})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('productname')
        product.price = request.POST.get('price')
        if 'productimage' in request.FILES:
            product.image = request.FILES.get('productimage')
        product.detail = request.POST.get('detail')
        category_id = request.POST.get('category')
        product.category = category.objects.get(id=category_id)
        product.save()
        return redirect('admin_page')
    categories = category.objects.all()
    return render(request, 'edit_product.html', {'product': product, 'categories': categories})
