from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from math import ceil
import json

# importing Product from models
from . models import Contact, Product, Order, OrderUpdate

# this function is for slides and settings items as a pair of 4 and not putting them using categories

# def index(request):
#     products = Product.objects.all()
#     n = len(products)
#     nSlides = n//4 + ceil((n/4)+( n//4))
#     params = {'nSlides': nSlides , 'range' : range(0 , nSlides), 'product': products }
#     return render(request , 'shop/index.html', params)

def index(request):
    allProds = []
    catprods = Product.objects.values('product_subcat', 'product_id')
    cats = {item['product_subcat'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_subcat=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)

def productview(request, product_id):
    product = Product.objects.filter(product_id=product_id)
    return render(request, 'shop/productview.html', {'product': product})

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    # to get input from user we uses "POST"
    # after taking input data of user "Contact Us" make models for putting them into database and now
    # store all user input data to database using "contact = Contact(contact_name = name , contact_email = email , contact_phone = phone , contact_desc = desc)"
    if request.method == "POST":
        email = request.POST.get('email', "")
        name = request.POST.get('name', " ")
        phone = request.POST.get('phone', "")
        desc = request.POST.get('desc', " ")
        contact = Contact(contact_name=name, contact_email=email,
                          contact_phone=phone, contact_desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')

def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get("orderid", " ")
        email = request.POST.get("email", " ")

        try:
            order = Order.objects.filter(order_id=orderid, email=email)

            if len(order) > 0:
                # getting information corr. to orderid input by user
                update = OrderUpdate.objects.filter(order_id=orderid)

                # creating empty array
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].itemJson], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")
        except Exception as e:
            return HttpResponse(e)
    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')

def checkout(request):
    if request.method == "POST":
        itemJson = request.POST.get("itemJson")
        name = request.POST.get("name")
        email = request.POST.get("email")
        tel = request.POST.get("tel")
        address = request.POST.get("address1", " ") + \
            "" + request.POST.get("address2", " ")
        state = request.POST.get("state", " ")
        zip = request.POST.get("zip", " ")

        order = Order(itemJson=itemJson, name=name, email=email, tel=tel,
                      address=address, state=state, zip=zip)
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="the order has been placed ")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')
