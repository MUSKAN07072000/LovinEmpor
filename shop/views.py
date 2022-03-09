from . models import Contact, Product, Order, OrderUpdate, AboutUs
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from math import ceil
from paytm import checksum
import json
# for exempting payment request
from django.views.decorators.csrf import csrf_exempt
MERCHANT_KEY = '%G0NBeK1XrJCEuSF'

# importing Product from models

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

def about(request):
    head = AboutUs.objects.all()
    print(head)
    params = {'head' : head}
    return render(request, 'shop/about.html', params)

def searchMatch(query, item):
    if query in item.product_desc.lower() or query in item.product_name.lower() or query in item.product_cat.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('product_subcat', 'product_id')
    cats = {item['product_subcat'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(product_subcat=cat)
        prod = {item for item in prodtemp if searchMatch(
            query, item)}
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, 'msg': ""}
    if len(allProds) == 0 or len(query) < 3:
        params = {
            'msg': "sorry we are not able to fetch your items please make sure to write atleast 3 charactered word"}
    return render(request, 'shop/search.html', params)


def productview(request, product_id):
    product = Product.objects.filter(product_id=product_id)
    return render(request, 'shop/productview.html', {'product': product})


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
                    response = json.dumps(
                        [updates, order[0].itemJson], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")
        except Exception as e:
            return HttpResponse(e)
    return render(request, 'shop/tracker.html')


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
        amount = request.POST.get("amount", " ")

        order = Order(itemJson=itemJson, name=name, email=email, tel=tel,
                      address=address, state=state, zip=zip, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="your order has been placed ")
        update.save()
        thanks = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        
        # request paytm to transfer the amout to your account after payment by user
        param_dict = {

            'MID': 'CIFitL76578495492594',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict ,'%G0NBeK1XrJCEuSF' )
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post requestt here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            Checksum = form[i]

    verify = checksum.verify_checksum(response_dict,'%G0NBeK1XrJCEuSF',Checksum)
    if verify:
        if response_dict["RESPCODE"] == '01':
            print("order succesful")
        else:
            print("order was not successful because" +
                  response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
