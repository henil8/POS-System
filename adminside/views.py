from django.shortcuts import render, redirect,get_object_or_404
from .forms import CustomPasswordChangeForm,StaffRegisterForm,InventoryForm,PurchaseForm,UpatePasswordForm,UpdateUserForm
from .models import Branch,Inventory,Purchase,CustomUser,Categories,Tables,Supplier
from django.contrib.auth.forms import UserChangeForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum,Count,Max
from staffside.models import Sales_details,Sales_Report,Customer
from django.utils import timezone
from datetime import timedelta
import numpy as np
from staffside.models import Sales_details
from django.db.models.functions import TruncHour,TruncDay,TruncMonth
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required

def home(request):
    return redirect('adminside:dashboard')

@login_required(login_url='')
def render_page(request, template, data=None):
    if data is None:
        data={}
    return render(request, "adminside/base.html", {"template": template, "data":data})

@login_required(login_url='')
def dashboard(request):
    timezone.activate('Asia/Kolkata')
    today=timezone.now()
    print(today,'-----------------------------')
    weekly=timezone.now() - timedelta(days=7)
    print(weekly,'-----------------------')
    # monthly=timezone.now() - timedelta(days=30)
    monthly = timezone.now().replace(day=1)
    print(monthly,'-----------------')
    sales_details=Sales_Report.objects.all()
    
    # For Graph
    daily_sales=Sales_details.objects.filter(timeanddate__date=today).annotate(hour=TruncHour('timeanddate'))\
        .values('hour')\
        .annotate(total=Sum('total_amount'))\
        .order_by('hour')

    weekly_sales=Sales_details.objects.filter(timeanddate__date__gte=weekly.date()).annotate(day=TruncDay('timeanddate'))\
        .values('day')\
        .annotate(total=Sum('total_amount'))\
        .order_by('day')
    
    monthly_sales=Sales_details.objects.filter(timeanddate__date__gte=monthly.date()).annotate(month=TruncDay('timeanddate'))\
        .values('month')\
        .annotate(total=Sum('total_amount'))\
        .order_by('month')
    
    sales_time = [localtime(sale['hour']).strftime('%I %p') for sale in daily_sales]  # e.g., 10 AM, 11 AM
    sales_amount = [sale['total'] for sale in daily_sales]

    sales_last_week=[localtime(sale['day']).strftime('%d %b') for sale in weekly_sales] 
    sales_total_last_week=[(sale['total']) for sale in weekly_sales] 

    sales_last_month=[localtime(sale['month']).strftime('%d %b') for sale in monthly_sales] 
    sales_total_last_month=[(sale['total']) for sale in monthly_sales]
    # total_revenue=Sales_details.objects.aggregate(Sum('total_amount'))['total_amount__sum']
    # print(total_revenue,'********************')
    total_revenue_today=None
    total_revenue_this_week=None
    total_revenue_this_month=None

    filter='Today'
    if request.method=='POST':
      filter=request.POST.get('filter')


    print(filter,'__________________--')
    total_revenue_today=Sales_details.objects.filter(timeanddate__date=today).aggregate(Sum('total_amount'))['total_amount__sum']
    total_revenue_this_week=Sales_details.objects.filter(timeanddate__date__gte=weekly.date()).aggregate(Sum('total_amount'))['total_amount__sum']
    total_revenue_this_month=Sales_details.objects.filter(timeanddate__date__gte=monthly.date()).aggregate(Sum('total_amount'))['total_amount__sum']



    total_profit_today=Sales_Report.objects.filter(timeanddate__date=today).aggregate(Sum('profit'))['profit__sum']
    total_profit_this_week=Sales_Report.objects.filter(timeanddate__date__gte=weekly.date()).aggregate(Sum('profit'))['profit__sum']
    total_profit_this_month=Sales_Report.objects.filter(timeanddate__date__gte=monthly.date()).aggregate(Sum('profit'))['profit__sum']

    total_orders_today=Sales_details.objects.filter(timeanddate__date=today).aggregate(Count('order_id'))['order_id__count']
    total_orders_this_week=Sales_details.objects.filter(timeanddate__date__gte=weekly.date()).aggregate(Count('order_id'))['order_id__count']
    total_orders_this_month=Sales_details.objects.filter(timeanddate__date__gte=monthly.date()).aggregate(Count('order_id'))['order_id__count']
   
    # For Chart
    Food=Sales_Report.objects.exclude(category__in=['Refreshments','Deserts'] ).aggregate(Sum('quantity'))['quantity__sum']
    Refreshments=Sales_Report.objects.filter(category='Refreshments').aggregate(Sum('quantity'))['quantity__sum']
    Deserts=Sales_Report.objects.filter(category='Deserts').aggregate(Sum('quantity'))['quantity__sum']
    # Total=Sales_Report.objects.aggregate(Sum('quantity'))['quantity__sum']

   # For Trending Dishes
    todays_trending_dishes=Sales_Report.objects.filter(timeanddate__date=today).values('item_name').annotate(quantity=Sum('quantity')).order_by('-quantity')[:3]
    this_weeks_trending_dishes=Sales_Report.objects.filter(timeanddate__date__gte=weekly.date()).values('item_name').annotate(quantity=Sum('quantity')).order_by('-quantity')[:3]
    this_months_trending_dishes=Sales_Report.objects.filter(timeanddate__date__gte=monthly.date()).values('item_name').annotate(quantity=Sum('quantity')).order_by('-quantity')[:3]

    # todays_trending_dishes=todays_trending_dishes.filter(item_name=todays_trending_dishes.aggregate(Max('quantity')))
    print(todays_trending_dishes,'----------------------')
    print(this_weeks_trending_dishes,'&&&&&&&&&&&&&&&&&&&&&&&')
  

    best_employees=Sales_details.objects.values('staff_name').annotate(total_orders=Count('order_id')).order_by('-total_orders')[:3]

    context={
        "filter":filter,
        "sales_time":list(sales_time),
        "sales_amount":list(sales_amount),
        "sales_last_week":sales_last_week,
        "sales_total_last_week":sales_total_last_week,
        "sales_last_month":sales_last_month,
        "sales_total_last_month":sales_total_last_month,
        "total_revenue_today":total_revenue_today,
        "total_revenue_this_week":total_revenue_this_week,
        "total_revenue_this_month":total_revenue_this_month,
        "total_profit_today":total_profit_today,
        "total_profit_this_week":total_profit_this_week,
        "total_profit_this_month":total_profit_this_month,
        "total_orders_today":total_orders_today,
        "total_orders_this_week":total_orders_this_week,
        "total_orders_this_month":total_orders_this_month,
        "Food":Food,
        "Refreshments":Refreshments,
        "Deserts":Deserts,
        "todays_trending_dishes":todays_trending_dishes,
        "this_weeks_trending_dishes":this_weeks_trending_dishes,
        "this_months_trending_dishes":this_months_trending_dishes,
        "best_employees":best_employees
    }


    return render_page(request, 'adminside/dashboard.html',context)



@login_required(login_url='')
def branches(request):  
    branches=Branch.objects.all()
    context={
        "branches":branches

    }
    if request.method=='POST':
       location=request.POST.get("location")
       area=request.POST.get("storeArea")
       managerID=request.POST.get("managerID")
       PhoneNo=request.POST.get("PhoneNo")
       status=request.POST.get("status")
       Br=Branch(location=location,area=area,manager_id=managerID,phone_no=PhoneNo,status=status)
       Br.save()       
       return redirect('/adminside/branches/')
 
    

    return render_page(request, 'adminside/branches.html',context)



def update_branch(request):
        branch_id = request.POST.get("branchID")
        branch=Branch.objects.get(id=branch_id)

        if request.method=='POST':
            branch.location=request.POST.get("location")
            branch.area=request.POST.get("storeArea")
            branch.manager_id=request.POST.get("managerID")
            branch.phone_no=request.POST.get("PhoneNo")
            branch.status=request.POST.get("status")
            branch.save()       
            return redirect('/adminside/branches/')

        return redirect('/adminside/branches/')

def delete_branch(request):
    
    if request.method=='POST':
      branch_id=request.POST.get("bID")
      print(branch_id)
      branch=Branch.objects.get(id=branch_id)
      branch.delete()
      return redirect('/adminside/branches/')
    return redirect('/adminside/branches/')

@login_required(login_url='')
def suppliers(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        supplierName = request.POST.get('supplierName')
        companyName = request.POST.get('companyName')
        supplierEmail = request.POST.get('supplierEmail')
        supplierAddress= request.POST.get('supplierAddress')
        supplierPhone = request.POST.get('supplierPhone')
        supplierStore=request.POST.get('supplierStore')
 
        SP=Supplier(supplier_name=supplierName,company_name=companyName,supplier_email=supplierEmail,
                    address=supplierAddress,supplier_phone=supplierPhone,branch=supplierStore)
        SP.save()
        return redirect('adminside:suppliers')
  
    branch=Branch.objects.all()
    query=request.GET.get('q')
    if query:
        suppliers=Supplier.objects.filter(supplier_name__icontains=query) | Supplier.objects.filter(company_name__icontains=query)
    else:
        suppliers=Supplier.objects.all().order_by('id')

    context={
        "suppliers":suppliers,
        "branch":branch
    }

    print(context)
    return render_page(request, 'adminside/suppliers.html',context)

def update_supplier(request):
    id=request.POST.get("supplierID")
    supplier=Supplier.objects.get(id=id)
    if request.method == 'POST':
        supplier.id=request.POST.get('supplierID')
        supplier.supplier_name = request.POST.get('updateName')
        supplier.company_name = request.POST.get('updateCompany')
        supplier.supplier_email = request.POST.get('update_email')
        supplier.address= request.POST.get('update_address')
        supplier.supplier_phone = request.POST.get('update_phone')
        supplier.branch = request.POST.get('update_branch')
        supplier.save()
        return redirect("/adminside/suppliers")
    return redirect("/adminside/suppliers")

import logging



def delete_supplier(request):
    if request.method == 'POST':
        id = request.POST.get('SupID')
        supplier= get_object_or_404(Supplier, pk=id)
        supplier.delete()        
        return redirect('adminside:suppliers')


@login_required(login_url='')
def purchase(request):    
    form= PurchaseForm()
    if request.method=='POST':
        form=PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/adminside/purchase/')
        else:
          messages.error(request,"Invalid Details")
    purchases=Purchase.objects.all()
    context={
        "form":form,
        "purchases":purchases
    }

    return render_page(request, 'adminside/purchase.html',context)
def update_purchase(request):
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id')
        purchase = Purchase.objects.get(id=purchase_id)
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully.")
            return redirect('/adminside/purchase/')

        else:
            print(form.errors,'------------------------')
            messages.error(request, "Invalid data.")
            return redirect('/adminside/purchase/')

def delete_purchase(request):
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id')   
        purchase = Purchase.objects.filter(id=purchase_id).first()
        if purchase:
            purchase.delete()
            messages.success(request, "Purchase deleted successfully.")
        else:
           pass
    return redirect('/adminside/purchase/')

@login_required(login_url='')
def categories(request):
    if request.method=='POST':
        # cat_id=request.POST.get('ID')
        name=request.POST.get('name')
        status=request.POST.get('status')
        # print(cat_id,name,status)
        ct=Categories(category_name=name,status=status)
        ct.save()
        return redirect('/adminside/categories/')
    categories=Categories.objects.all()
    context={
        "categories":categories
    }

    return render_page(request, 'adminside/categories.html',context)

def update_category(request):
    cat_id = request.POST.get("itemID")
    print(cat_id)
    category=Categories.objects.get(id=cat_id)
    if request.method=='POST':
        # category.category_id=request.POST.get("itemIDDisplay")
        category.category_name=request.POST.get("name")
        category.status=request.POST.get("status")
        category.save()       
        return redirect('/adminside/categories/')

    return redirect('/adminside/categories/')

def delete_category(request):
    
    if request.method=='POST':
      cat_id=request.POST.get("iID")
    #   print(branch_id)
      category=Categories.objects.get(id=cat_id)
      category.delete()
      return redirect('/adminside/categories/')
    return redirect('/adminside/categories/')


@login_required(login_url='')
def inventory(request):
    form=InventoryForm()
    if request.method=='POST':
        form=InventoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/adminside/inventory/')
        else:
            messages.error(request,"Invalid Details")
    
    inventory=Inventory.objects.all().order_by('id')
    context={
        "form":form,
        "inventory":inventory
    }
    return render_page(request, 'adminside/inventory.html',context)

def update_inventory(request):
    id=request.POST.get('id')
    fi=Inventory.objects.get(id=id)
    
    form=InventoryForm(instance=fi)
    if request.method=='POST':
        form=InventoryForm(request.POST,request.FILES,instance=fi)
        if form.is_valid():
            form.save()
            return redirect('/adminside/inventory/')
    context={
        "form":form
    }
    return render(request, 'adminside/inventory.html', context)

def get_update_form(request, id):
    item = Inventory.objects.get(id=id)  # Fetch the specific item
    form = InventoryForm(instance=item)  # Prefill the form with the item data
    return HttpResponse(form.as_p()) 

@login_required(login_url='')
def fooditems(request): 

    inventory=Inventory.objects.all().order_by('id')

    context={
        "inventory":inventory
    }
    return render_page(request, 'adminside/fooditems.html',context)


@login_required(login_url='')
def customer(request):
    customers = Customer.objects.all().order_by('-id')

    context={
        "customers":customers
    }
    return render_page(request, 'adminside/customer.html',context)

def staff(request):
    form=StaffRegisterForm(initial={
        'first_name': None,
        'last_name': None,
        'email': None,
        'role': None,
        'phone_no': None,
        'username': None,
        'password1': None,
        'password2': None
    })
    if request.method=='POST':
        form=StaffRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('/adminside/staff/')
        else:
            messages.error(request,("Please correct the errors below."))
    staff_details=Sales_details.objects.values('staff_name').annotate(total_orders=Count('order_id'),sales=Sum('total_amount'))      
    staffs=CustomUser.objects.all().order_by('id')
    context={
        "form":form,
        "staffs":staffs,
        "staff_details":staff_details
    }
    return render_page(request, 'adminside/staff.html',context)

def delete_staff(request):
    if request.method=='POST':
      staff_id=request.POST.get("staff_id")
      if not staff_id:  # If no ID is received
            print("Error: No staff ID received.")
            return HttpResponse("Staff ID is missing.", status=400)  # Bad Request
      print(staff_id)
      staff=CustomUser.objects.get(id=staff_id)
      staff.delete()
      return redirect('/adminside/staff/')
    return redirect('/adminside/staff/')

@login_required(login_url='')
def tables(request):
    tables=Tables.objects.all().order_by('table_id')
    if request.method=='POST':
        Table_no=request.POST.get('table_id')
        seats=request.POST.get('seats')
        status=request.POST.get('status')
        tb=Tables(table_id=Table_no,seats=seats,status=status)
        tb.save()
    
        return redirect('/adminside/tables/')
    context={
        "Tables":tables,
    }
    return render_page(request,'adminside/tables.html',context)

def update_table(request):
    if request.method=='POST':
        table_id=request.POST.get('tabId')
        table=Tables.objects.get(id=table_id)
        table.table_id=request.POST.get('Table_id')
        table.seats=request.POST.get('seats')
        table.status=request.POST.get('status')
        table.save()
        return redirect('/adminside/tables/')
    
def delete_table(request):
    if request.method=='POST':
        table_id=request.POST.get('tID')
        table=Tables.objects.get(id=table_id)
        table.delete()
        return redirect('/adminside/tables/')

@login_required(login_url='')
def reports(request):
    filter=None
    sales_data=Sales_Report.objects.all()
    sales_data1=Sales_Report.objects.values('item_id','item_name','category').annotate(quantity=Sum('quantity'),profit=Sum('profit'))
    if request.method=='POST':
        filter=request.POST.get('filter')
        queryset = Sales_Report.objects.values(
            'item_id', 'item_name', 'category'
        ).annotate(
            quantity=Sum('quantity'),
            profit=Sum('profit')
        )
        if filter == 'MaxQuantitySold':
            max_q = queryset.order_by('-quantity').first()
            sales_data1 = [max_q] if max_q else []
        elif filter == 'MinQuantitySold':
            min_q = queryset.order_by('quantity').first()
            sales_data1 = [min_q] if min_q else []
        elif filter == 'MaxProfitFooditem':
            max_p = queryset.order_by('-profit').first()
            sales_data1 = [max_p] if max_p else []
        elif filter == 'MinProfitFooditem':
            min_p = queryset.order_by('profit').first()
            sales_data1 = [min_p] if min_p else []
        elif filter == 'default':
            min_p = queryset
            sales_data1 = min_p
    context={
        'sales_data':sales_data,
        'sales_data1':sales_data1,
        'filter':filter
    }
    return render_page(request, 'adminside/reports.html',context)


def low_stock_notifications(request):
    threshold = 20  # or 30 if you want
    low_stock_items = Inventory.objects.filter(quantity__lt=threshold)
    return render_page(request, 'adminside/low_stock.html', {
        'low_stock_items': low_stock_items,
    })


def adminside_settings_view(request):
    return redirect('adminside:profile')

@login_required(login_url='')
def render_settings_page(request, template, context=None):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, template, context or {})
    context = context or {}
    context["template"] = template  # Ensures `template` is still passed
    return render(request, "adminside/settings.html", context)

def change_password(request):
    current_user=request.user
    form = UpatePasswordForm(user=current_user)
    if request.method=='POST':
       form=UpatePasswordForm(user=current_user,data=request.POST)
       if form.is_valid():
           form.save()
           update_session_auth_hash(request,form.user)
           messages.success(request,('Password have been changed successfully'))
           return redirect('/adminside/change_password/')
       else:
          messages.error(request,('Please correct the errors below'))
          print(form.errors,'-------------------------')
    
     
    context={
        "form":form
    }  
    return render_settings_page(request, "adminside/settings/change_password.html", context)


def edit_profile(request):
    return render_settings_page(request,"adminside/settings/edit_profile.html")

@login_required(login_url='')
def profile(request):
    timezone.activate('Asia/Kolkata')
    user_form=UpdateUserForm(request.user)

    if request.user.is_authenticated:
        current_user=CustomUser.objects.get(id=request.user.id)
        user_form=UpdateUserForm(request.POST or None,instance=current_user)
        if user_form.is_valid():
             user_form.save()
             messages.success(request,'User details have  been  Updated  successfully')
             return redirect('/adminside/profile/')
    context={
        "user_form":user_form   
    }
    return render_settings_page(request,"adminside/settings/profile.html",context)

def save_image(request,id):
    if request.method=="POST" and request.FILES :
        image=request.FILES.get('image')
        current_user=CustomUser.objects.get(id=id)
        current_user.image=image
        current_user.save()
        messages.success(request,'Image is uploaded successfully')
        return redirect('/adminside/profile/')

def logout_view(request):
    sales_data = [
    {"invoice_no": "101", "full_name": "John Doe", "phone": "9876543210", "email": "john.doe@example.com", "total": "450", "paid": "200", "balance": "250", "date": "01/15"},
    
    ]
    return render_page(request, 'adminside/logout.html',data=sales_data)

def login_view(request):
    form=AuthenticationForm()
    if request.method=='POST':
        
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
           username=form.cleaned_data.get('username')
           password=form.cleaned_data.get('password')
           user=authenticate(request,username=username,password=password)
           if user is not None:
            

               
            #    print(f"User: {user.username}, is_staff: {user.is_staff}, is_superuser: {user.is_superuser}")
                 
               login(request,user)
              
               if user.is_staff:
                   return redirect('adminside:dashboard')
               else:
                   return redirect('staffside:pos')
            
        
           else:
               messages.error(request,"Invalid username or password") 
               return redirect('adminside:login')
    context={
        "form":form
    }

    return render(request,'adminside/login.html',context)

def logout_user(request):
    logout(request)
    return redirect('adminside:login')