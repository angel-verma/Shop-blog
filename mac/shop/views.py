from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, orderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
# from paytm import checksum
MERCHANT_KEY = ''


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


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method == "POST":
        # print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        msg = request.POST.get('msg', '')
        # print(name, email, phone, msg)
        contact = Contact(name=name, email=email, phone=phone, msg=msg)
        contact.save()
        thank = True

    return render(request, 'shop/contact.html', {'thank':thank})


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
                    response = json.dumps(updates,order[0].itemsJson, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def productView(request, id):
    # Fetch the products using the id
    product = Product.objects.filter(id=id)
    print(product)
    return render(request, 'shop/prod-view.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        # print(request)
        itemsJson = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        _zip = request.POST.get('_zip', '')
        phone = request.POST.get('phone', '')
        # print(name, email, phone, msg)
        order = Order(itemsJson=itemsJson, name=name, email=email, address=address,
                      city=city, state=state, _zip=_zip, phone=phone, amount=amount)
        order.save()
        update = orderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed!")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})

        # Request paytm to transfer the amount to your account after payment by user
        # param_dict = {

        #         'MID': 'Your-Merchant-Id-Here',
        #         'ORDER_ID': str(order.order_id),
        #         'TXN_AMOUNT': str(amount),
        #         'CUST_ID': email,
        #         'INDUSTRY_TYPE_ID': 'Retail',
        #         'WEBSITE': 'WEBSTAGING',
        #         'CHANNEL_ID': 'WEB',
        #         'CALLBACK_URL':'http://127.0.0.1:8000/shop/handle_request/',

        # }
        # param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
