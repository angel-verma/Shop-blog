from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, orderUpdate
from math import ceil
import json


def index(request):
    # products = Product.objects.all()
    # print(products)

    # n = len(products)
    # nSlides = n//4+ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4+ceil((n/4)-(n//4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides': nSlides,
    #           'range': range(1, nSlides), 'product': products}

    # allProds = [ [products, range(1, nSlides), nSlides],
    #              [products, range(1, nSlides), nSlides] ]

    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        # print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        msg = request.POST.get('msg', '')
        # print(name, email, phone, msg)
        contact = Contact(name=name, email=email, phone=phone, msg=msg)
        contact.save()

    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email', '')
        return HttpResponse(f"{order_id} and {email}")
        try:
            order = Orders.objects.filter(order_id=order_id, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def productView(request, id):
    # Fetch the products using the id
    product = Product.objects.filter(id=id)
    print(product)
    return render(request, 'shop/prod-view.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        # print(request)
        itemsJson = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        _zip = request.POST.get('_zip', '')
        phone = request.POST.get('phone', '')
        # print(name, email, phone, msg)
        order = Order(itemsJson=itemsJson, name=name, email=email, address=address,
                      city=city, state=state, _zip=_zip, phone=phone)
        order.save()
        update = orderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed!")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})

    return render(request, 'shop/checkout.html')
