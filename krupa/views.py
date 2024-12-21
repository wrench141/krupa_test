from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
import json
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer
from .serializer import *
from .serializer import SupportTicketSerializer
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.serializers import serialize
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import uuid
from django.conf import settings
import os

# Create your views here.
# @csrf_exempt
import json
from django.http import JsonResponse

def login_view(request):
    if request.method == "POST": 
        # Parse the JSON payload
        print("Request body:", request.body)

        data = json.loads(request.body)
        identity_value = data.get("identities", [{}])[0].get("identityValue", None)
        
        # Ensure the number is valid
        if identity_value:
            number = identity_value[-10:]
            print("Extracted number:", number)
            
            try:
                user = CustomUser.objects.get(phone_number=number)
                print(user)
            except CustomUser.DoesNotExist:
                print("User with this phone number does not exist")
                return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=400)
            
            # Check if the user is valid and active
            if user:
                print("Logging in user:", user)
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Login successful'})
            else:
                print("User is inactive or invalid")
                return JsonResponse({'status': 'error', 'message': 'User is inactive'}, status=400)
        else:
            print("Invalid identity value")
            return JsonResponse({'status': 'error', 'message': 'Invalid identity value'}, status=400)
    
    return render(request, "otp.html")


def register_view(request):  # sourcery skip: avoid-builtin-shadow
    if request.method == "POST":
        try:
            return _extracted_from_register_view_4(request)
        except IntegrityError:
            return JsonResponse({'success':False,"error":"Email already exits"},status = 400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({'success':False,"error": str(e)},status = 500)

    return render(request, 'register.html')


# TODO Rename this here and in `register_view`
def _extracted_from_register_view_4(request):
    data = json.loads(request.body)
    print(data)
    if CustomUser.objects.filter(email = data['email']).exists():
        return JsonResponse({'success':False,"error":"Email already exits"},status = 400)
    user = CustomUser.objects.create(
        email = data['email'],
        # password = data['password'],
        gstin = data['gstin'],
        username = data['email'],
        phone_number = data['phone']
    )
    user.set_password(data['password'])
    user.save()
    context = {'id', user.id}
    return JsonResponse({'success': True, 'redirect_url': '/'})

@login_required(login_url='/login/')
def order_details_view(request, id,id2):
        user_details = Orders.objects.filter(order_id=id).first()
        est = user_details.estimate
        address = Estimate.objects.get(id=est.id)
        context = {'id': id2, 'address': address,"user_details":user_details}
        return render(request, "oder_details.html", context)

@login_required(login_url='/login/')
def order_view(request, id):
    if request.user.id == id:
        try:
            user = CustomUser.objects.get(id=id)
            orders = Orders.objects.filter(profile=user)
            serializer = OrdersSerializer(orders, many=True)
            orders_json = JSONRenderer().render(serializer.data)
            context = {
                'orders': orders_json.decode('utf-8'),
                'id': id,
                'order_id': orders[0].id if orders.exists() else None
            }
        except Orders.DoesNotExist:
            context = {'error': 'Order not found'}
        except Exception as e:
            context = {'error': str(e)}
        return render(request, 'order.html', context)
    else:
        return redirect('/login/')

@login_required(login_url='/login/')
def products_view(requset):  # sourcery skip: avoid-builtin-shadow
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    products = Products.objects.all()
    subcategory_json = SubcategorySerializer(subcategory,many = True)
    subcategory_json1 = JSONRenderer().render(subcategory_json.data)
    serializer = ProductSerializer(products, many=True)
    products_json = JSONRenderer().render(serializer.data)
    context = {'id':requset.user.id ,'category':category,'subcategory':subcategory, 'product':products_json.decode('utf-8'),'subcategory1':subcategory_json1.decode('utf-8')}
    if requset.method == "POST":
        data = requset.POST
        print(data)
        product_name_1 = data.get("product")
        product_name = Products.objects.get(product_name = product_name_1)
        quantity = data.get("quantity")
        company = data.get("company")
        pincode = data.get("pincode")
        email = data.get("email")
        mobile_number = data.get("mobile")
        profile = CustomUser.objects.filter(id=requset.user.id).first()
        type = data.get('type')
        request_model = Request.objects.create(
            profile = profile,
            product_name = product_name,
            quantity = quantity,
            company = company,
            pincode = pincode,
            email = email,
            mobile_number = mobile_number,
            type = type
        )
        request_model.save()
        request_model.requestid = f"RFQ-{request_model.id}"
        request_model.save()
    return render(requset,"products.html",context)


@login_required(login_url='/login/')
def request_view(request, id):
    if request.user.id == id:
        profile = CustomUser.objects.get(id=id)
        requests = Request.objects.filter(profile=profile)
        address = UserAddress.objects.filter(profile = profile).first()
        shipadd = ShippingAddress.objects.filter(profile = profile)
        context = {'id': id, 'requests': requests,'address':address,'shipadd':shipadd}
        if request.method == "POST":
            data1 = request.POST
            print(data1)
            if "shipping-add" in data1:
                data = data1.get('shipping-add')
                rfqs1 = data.split(',')[0]
                rfq = Request.objects.get(requestid = rfqs1)
                address1 = ShippingAddress.objects.get(id = int(data.split(',')[1]))
                rfq.shipping = address1
                rfq.save()
                shippinadd = f"{address1.company_name}\n{address1.address_type}\n{address1.street_address}\n{address1.city}\n{address1.state}"

            else:
                rfq = Request.objects.get(requestid = data1.get('rfq_id'))
                address1 = ShippingAddress.objects.create(
                        profile = profile,
                        company_name=data1.get('company-n'),  # Adjust based on your need
                        address_type=data1.get('address_type'),
                        street_address=data1.get('street_address'),
                        city=data1.get('city'),
                        state=data1.get('state')
                )
                address1.save()
                rfq.shipping = address1
                rfq.save()
                shippinadd = f"{address1.company_name}\n{address1.address_type}\n{address1.street_address}\n{address1.city}\n{address1.state}"
            print(shippinadd)
            est = Estimate.objects.filter(request = rfq).last()
            print(est.shipping_address)
            est.shipping_address = shippinadd
            print(est.shipping_address)
            est.save()
            return redirect(f'/request/{id}/')
        return render(request, "request.html", context)
    else:
        return redirect('/login/')

@login_required(login_url='/login/')
def support_ticket_view_1(request, id):
    if request.user.id == id:
        profile = CustomUser.objects.get(id=id)
        tickets = SupportTicket.objects.filter(profile=profile)
        context = {'id': id, 'tickets': tickets}
        return render(request, "supportticket.html", context)
    else:
        return redirect('/login/')

@login_required(login_url='/login/')
def support_ticket_view_2(request, id):
    if request.user.id == id:
        profile = CustomUser.objects.get(id=id)
        context = {'id': id}
        if request.method == "POST":
            data = request.POST
            ticket = SupportTicket.objects.create(
                profile=profile,
                department=data.get("department"),
                subject=data.get("subject"),
                message=data.get("message"),
                additional_email=data.get("email-recipients")
            )
            ticket.save()
            return redirect(f'/support/{id}/')
        return render(request, "supportticket1.html", context)
    else:
        return redirect('/login/')



@login_required(login_url='/login/')
def account_view(request, id):
    if request.user.id != id:
        return redirect('/login/')
    
    data = CustomUser.objects.get(id=id)
    req = Request.objects.filter(profile=data)
    info = CompanyInfo.objects.filter(user=data).first()

    if request.method == "POST":
        data1 = request.POST

        # Handle Company Info Form Submission
        if 'company_name' in data1:
            if CompanyInfo.objects.filter(user=data).exists():
                cmpy_info = CompanyInfo.objects.filter(user=data).first()
                cmpy_info.company_name = data1.get('company_name')
                cmpy_info.pan = data1.get('pan_number')
                cmpy_info.gstno = data1.get('gst_number')
                cmpy_info.cinno = data1.get('cin_number')
                messages.success(request, "Company info updated successfully.")
            else:
                cmpy_info = CompanyInfo.objects.create(
                    user=data,
                    company_name=data1.get('company_name'),
                    pan=data1.get('pan_number'),
                    gstno=data1.get('gst_number'),
                    cinno=data1.get('cin_number')
                )
                messages.success(request, "Company info created successfully.")
            cmpy_info.save()
            info = cmpy_info  # Update `info` after saving or creating company info

        # Handle Address Form Submission
        elif 'address_type' in data1:  # Check for the address form
            # if UserAddress.objects.filter(profile = data).exists():
            #     add = UserAddress.objects.filter(profile = data).first()
            #     add.company_name = data1.get('company-n')
            #     add.address_type=data1.get('address_type')
            #     add.street_address=data1.get('street_address')
            #     add.city=data1.get('city')
            #     add.state=data1.get('state')
            #     add.save()
            # else:
                address1 = UserAddress.objects.create(
                    profile=data,
                    company_name=data1.get('company-n'),  # Adjust based on your need
                    address_type=data1.get('address_type'),
                    street_address=data1.get('street_address'),
                    city=data1.get('city'),
                    state=data1.get('state')
                )
                address1.save()

        return redirect("accounts", id=id)

    address = UserAddress.objects.filter(profile=data)
    context = {'data': data, 'address': address, 'id': id, 'req': req, 'info': info}
    return render(request, "accounts.html", context)


@login_required(login_url='/login/')
def Billing(request, id):
    if request.user.id != id:
        return redirect('/login/')
    
    user = CustomUser.objects.get(id=id)
    estimate = Estimate.objects.filter(customer_name=user)
    salesorder = SalesOrder.objects.filter(customer_name=user)
    invoiceEstimate = InvoiceEstimate.objects.filter(customer_name=user)
    context = {'estimates': estimate, 'salesorder': salesorder, 'invoiceEstimate': invoiceEstimate, 'id': id}
    return render(request, "billing.html", context)


@login_required(login_url='/login/')
def invoice_view(request, id, invid, name):
    if request.user.id != id:
        return redirect('/login/')
    
    if name == "estimate":
        estimate = Estimate.objects.get(id=invid)
        item = EstimateItem.objects.filter(estimate=estimate)
        context = {"objs": estimate, 'item': item, 'id': id, 'invoice': 'estimateinvoice','invid':invid,"img":None}
    elif name == "sales":
        sales = SalesOrder.objects.get(id=invid)
        item = SalesOrderItem.objects.filter(sales_order=sales)
        context = {"objs": sales, 'item': item, 'id': id, 'invoice': 'salesinvoice','invid':invid, "img":None}
    elif name == "invoice":
        invoice = InvoiceEstimate.objects.get(id=invid)
        img = invoice.attachement
        print(img)
        item = Item.objects.filter(invoice=invoice)
        context = {"objs": invoice, 'item': item, 'id': id, 'invoice': 'realinvoice','invid':invid,"img":img}
    return render(request, "invoice.html", context)


@login_required(login_url='/login/')
def dashboard_view(request, id):
    if request.user.id != id:
        return redirect('/login/')
    
    user = CustomUser.objects.get(id=id)
    estimate = Estimate.objects.filter(customer_name=user)
    salesorder = SalesOrder.objects.filter(customer_name=user)
    invoiceEstimate = InvoiceEstimate.objects.filter(customer_name=user)
    requests = len(Request.objects.filter(profile=user))
    orders = len(Orders.objects.filter(profile=user))
    context = {
        'estimates': estimate,
        'salesorder': salesorder,
        'invoiceEstimate': invoiceEstimate,
        'id': id,
        'requests': requests,
        'orders': orders
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='/login/')
def TrackHome(request, id):
    if request.user.id != id:
        return redirect('/login/')
    
    return render(request, "Track1.html", {'id': id})


@login_required(login_url='/login/')
def TrackOrder(request, id):
    if request.user.id != id:
        return redirect('/login/')
    
    return render(request, "Track2.html", {'id': id})
