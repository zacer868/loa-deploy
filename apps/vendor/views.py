from itertools import product
from unicodedata import name
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.shortcuts import get_object_or_404, redirect, render


from .forms import VendorForm
from .models import Info
from .models import Vendor
from apps.product.models import Product

from .forms import ProductForm

def info_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('become_vendor')
    else:
        form = VendorForm()
    return render(request, 'vendor/info_vendor.html', {'form' : VendorForm})



def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('vendor_admin')

    else:
        form = UserCreationForm()
    return render(request, 'vendor/become_vendor.html', {'form': form})

@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()


    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = False

        # for item in order.items.all():
        #     if item.vendor == request.user.vendor:
        #         order.vendor_paid_amount += item.get_total_price()

    return render(request, 'vendor/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders':orders })

@login_required
def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()

    return redirect('vendor_admin')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()

    return render(request, 'vendor/add_product.html', {'form': form})

@login_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        email = request.POST.get('email', '')

        if name:
            vendor.created_by.email = email
            vendor.created_by.save()


            return redirect('vendor_admin')

    return render(request, 'vendor/edit_vendor.html', {'vendor':vendor})

def vendors(request):
    vendors = Vendor.objects.all()

    return render(request, 'vendor/vendors.html', {'vendors': vendors})

def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    return render(request, 'vendor/vendor.html', {'vendor': vendor})