from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TableForm,UpdateUserForm,UpatePasswordForm,CustomPasswordChangeForm,CustomerForm
from django.contrib import messages
from django.contrib.auth import logout,update_session_auth_hash
from adminside.models import Inventory
from django.shortcuts import redirect, get_object_or_404
from django import template
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Sum,Count,Max
from .models import Cart,cart_items,order_details,Orders,Sales_Report,Sales_details,Customer
from adminside.models import Inventory,Categories,Tables,CustomUser
from django.contrib.auth.decorators import login_required


def home(request):
    # return HttpResponse("<h1>hello</h1>")
    return redirect('staffside:pos')

def render_page(request, template, data=None):
    return render(request, "staffside/base.html", {"template": template, "data":data})

@login_required(login_url='/staffside/')
def orders(request):
    orders=Orders.objects.all()
    Order_details=order_details.objects.all()
    cart=cart_items.objects.all()
    order_info=None
    table_id=None
    if request.method=="POST":
        table_id=request.POST.get('Table_id') 
        order_info=order_details.objects.filter(Table_id__Table_id=table_id)
        cart=cart_items.objects.filter(Table_id__Table_id=table_id)

    for order in orders:
        total=0
        details = order_details.objects.filter(Table_id=order.pk)
        for i in details:
            total=total+(i.quantity*i.price)
        setattr(order, 'total', total) 

    context={
        "orders":orders,
        "Order_details":Order_details,
        "order_info":order_info,
        "selected_table":table_id,
        "cart":cart,
    }
    return render_page(request, 'staffside/orders.html',context)


def orders_taken(request):
    Table_id=request.POST.get('Table_id') or request.session.get('table_no')
    print(Table_id,'((((((((((((((((((((((((((()))))))))))))))))))))))))))')
    cate_name=request.GET.get('cate_name')
    customer_name = request.POST.get("customer_name")
    Table_details=cart_items.objects.filter(Table_id__Table_id=Table_id)
    print(Table_details,'#####################')

    order,created = Orders.objects.get_or_create(Table_id=Table_id, defaults={'name':customer_name})
    
    item_details=order_details.objects.filter(Table_id__Table_id=Table_id).values_list('item_name',flat=True)
    print(item_details,"--------------------")
    for items in Table_details:
        if items.item_name in item_details:
           continue
        ord=order_details(Table_id=order,item_name=items.item_name,quantity=items.quantity,price=items.price)
        ord.save()
    messages.success(request,'Order Placed Successfully')
    return redirect(f'/staffside/pos/?table_no={Table_id}')

def save_changed_order(request):
    if request.method=="POST":
        if "Table_id" in request.POST:
                table_id=request.POST.get('Table_id')
                
                print(request.POST.items())
                for key,value in request.POST.items():
                    if key.startswith('quantity_'):
                        print(key,value,'-----------------------')
                        item_id=key.split('_')[1]
                        item_name=key.split('_')[2]
                        new_qty=int(value)
                        order_details.objects.filter(id=item_id).update(quantity=new_qty) 

                        cart_item = cart_items.objects.filter(item_name=item_name, Table_id__Table_id=table_id)
                        if cart_item:
                            cart_item.update(quantity=new_qty)
                    
 
                messages.success(request,f"Order Updated successfully for Table {table_id}")
                
        if "delete_item" in request.POST:
                    item_id=request.POST.get('delete_item')
                    item_name=request.POST.get('delete_item_name')
                    table_id=request.POST.get('delete_table_id')
                    int_table_id=int(table_id.split()[1])
                    order_details.objects.filter(id=item_id).delete()

                    cart_item = cart_items.objects.filter(item_name=item_name, Table_id__Table_id=int_table_id)
                    if cart_item:
                        cart_item.delete()
                    
        return redirect('/staffside/orders/')

def cancel_order(request):
    if request.method=='POST':
        id=request.POST.get('order_id')
        order=Orders.objects.get(id=id)
        order.delete()
        return redirect ('/staffside/orders/')
        
   
def payment_page(request):
    table_no = request.GET.get('table_no')
    # print(table_no,'------------------')
    o_id=Orders.objects.values_list('Table_id',flat=True)
    o_id=f'Table {o_id}'
    print(o_id,'------------------------')
    if not table_no or not table_no.isdigit():
        messages.error(request, 'Order has not been taken yet or table not selected.')
        return redirect('/staffside/pos/')
    if table_no not in o_id:
        messages.error(request,'Order has not been taken for this Table')
        return redirect(f'/staffside/pos/?table_no={table_no}')
 
    orders = order_details.objects.filter(Table_id__Table_id=table_no)
    order_details_list = order_details.objects.filter(Table_id__Table_id=table_no)
    total=0
    total_items=0
    for i in order_details_list:
        total=total+(i.quantity*i.price)
        total_items=total_items+i.quantity 
    context={
        'orders': orders,
        'table_no': table_no,
        'total_price':total
    }
    return render_page(request, 'staffside/payment.html',context)


def confirm_payment(request):
    if request.method=='POST':
        table_no=request.POST.get('table_no')
        total_price=request.POST.get('total_price')


    context={
        'table_no':table_no,
        'total_price':total_price
    }
    return render_page(request,'staffside/payment_method.html',context)

def final_payment(request):
    timezone.activate('Asia/Kolkata')
    if request.method=="POST":
        table_no=request.POST.get('table_no')
        method=request.POST.get('method')
        total_price=request.POST.get('total_price')
        orders=order_details.objects.filter(Table_id__Table_id=table_no)
          
    s_gst=float(total_price)*0.025
    c_gst=float(total_price)*0.025  

    final_total_amount=float(total_price)+(float(total_price)*0.05)
    date=timezone.now().date()
    time=timezone.now().time()
    context={
        'table_no':table_no,
        'method':method,
        'orders':orders,
        'total_price':total_price,
        'sgst':s_gst,
        'cgst':c_gst,
        'final_total_anount':final_total_amount,
        'date':date,
        'time':time
    }
    print(context)
    return render_page(request,'staffside/bill.html',context)



def final_exit(request):
    timezone.activate('Asia/Kolkata')
    if request.method=='POST':
        table_no=request.POST.get('table_no')
        total_amount=request.POST.get('total_amount')
        method=request.POST.get('method')
        orders_list=order_details.objects.filter(Table_id__Table_id=table_no)
        order_id=Orders.objects.get(Table_id=table_no)
        o_name=Orders.objects.filter(Table_id=table_no).values('name')
        print(order_id.pk,'-----------------------------')
        cart_id=Cart.objects.get(Table_id=table_no)
        print(order_id.Table_id,'_____________________')
        Item_names_in_s=Sales_Report.objects.values_list('item_name',flat=True)

        for o in orders_list:
            #  if o.item_name in Item_names_in_s:
            #     food_item=Inventory.objects.get(food_item_name=o.item_name)
            #     detail=Sales_Report.objects.get(item_name=o.item_name)  
            #     detail.quantity=detail.quantity+o.quantity
            #     detail.profit=detail.profit+((food_item.sell_price-food_item.cost_price)*o.quantity)
            #     detail.timeanddate=timezone.now()
            #     detail.save()
        
            #  else:
                food_item=Inventory.objects.get(food_item_name=o.item_name)
                profit=(food_item.sell_price-food_item.cost_price)*o.quantity
                s_r=Sales_Report(item_id=food_item.id,item_name=o.item_name,category=food_item.category,quantity=o.quantity,profit=profit,timeanddate=timezone.now())
                s_r.save()
                food_item.quantity=food_item.quantity-o.quantity
                food_item.save()
        s_d=Sales_details(order_id=order_id.pk,cust_name=o_name,total_amount=total_amount,staff_name=request.user.first_name,payment_method=method,timeanddate=timezone.now())
        s_d.save()
        order_id.delete()
        cart_id.delete()
        
           

        return redirect('/staffside/pos/')


@login_required(login_url='/staffside/')
def tables(request):
    tables=Tables.objects.all().order_by('table_id')
    Table_id=Orders.objects.values_list('Table_id',flat=True)
    table_orders=[]
    
    for table in tables:
        orders = order_details.objects.filter(Table_id__Table_id=table.table_id).values_list('item_name', flat=True)
        table_orders.append({"table_id": table.table_id,"items":list(orders) if orders else []}) 

    context={
        "tables":tables,
        "Table_id":Table_id,
        "table_orders":table_orders
    }
    

    return render_page(request, 'staffside/tables.html',context)

@login_required(login_url='/staffside/')
def pos(request):
    cate_name=request.GET.get('cate_name')
    print(cate_name,'--------------------')
    category_status=Categories.objects.filter(status='Available')
    if cate_name:
      inventory=Inventory.objects.filter(category=cate_name)
    else:
      inventory=Inventory.objects.all().order_by('id')
    cart=cart_items.objects.all()
    categories=Categories.objects.all().order_by('id')
    filter_cart=None
    selected_table=None
    order_details_list=None
    
    selected_table=request.GET.get('table_no')

    if selected_table:
        request.session['table_no'] = selected_table
    else:
        selected_table = request.session.get('table_no')

    cust_name=Orders.objects.filter(Table_id=selected_table).values('name')
    cust_name = cust_name[0]['name'] if cust_name else ''
    tables=Tables.objects.all().order_by('table_id')
    total=0
    total_items=0
    filter_cart=cart_items.objects.filter(Table_id__Table_id=selected_table) 
    order_details_list = order_details.objects.filter(Table_id__Table_id=selected_table)
    for i in filter_cart:
        total=total+(i.quantity*i.price)
        total_items=total_items+i.quantity  
    
    context={
        "inventory":inventory,
        "cart":cart,
        "filter_cart":filter_cart,
        "selected_table":selected_table,
        "categories":categories,
        "total":total,
        "total_items":total_items,
        "order_details":order_details_list,
        "cust_name":cust_name,
        "tables":tables,
        "Table_id": selected_table
        # "form":form
    }
    return render_page(request, 'staffside/pos.html',context)

def cart(request):
    cart=cart_items.objects.all()
    cate_name=request.GET.get('cate_name') or request.POST.get('cate_name')
    print(cate_name,'--------------------------------')
    if request.method=="POST":
        table_id=request.POST.get('Table_no')
        item_name=request.POST.get('itemName')
        quantity=int(request.POST.get('quantity'))
        item_price=float(request.POST.get('price'))
        if not table_id:
            messages.error(request,"Select  Table  first")
            return redirect(f'/staffside/pos/')
        filtered_table=cart.filter(Table_id=table_id)
        filtered_items=filtered_table.values_list('item_name',flat=True)
        print( filtered_items)

        cart_instance, created =Cart.objects.get_or_create(Table_id=table_id)
        
        if item_name in filtered_items:
            messages.error(request,"Food  Item  already  in  cart")
            return redirect(f'/staffside/pos/?table_no={table_id}&cate_name={cate_name}')     
             
                             
        critems=cart_items(Table_id=cart_instance,item_name=item_name,quantity=quantity,price=item_price)
        critems.save()
        return redirect(f'/staffside/pos/?table_no={table_id}&cate_name={cate_name}')
   
    return redirect(f'/staffside/pos/?table_no={table_id}&cate_name={cate_name}')


def add_quantity(request,item_name):
      print('Item name:',item_name)
      cate_name=request.GET.get('cate_name')
      table_id=request.GET.get('table_no')
      cart=cart_items.objects.filter(Table_id__Table_id=table_id)
      for cart_item in cart:
          if cart_item.item_name==item_name:
              cart_item.quantity+=1
              cart_item.save()
              return redirect(f'/staffside/pos/?table_no={table_id}&cate_name={cate_name}')

   
      return redirect(f'/staffside/pos/?table_no={table_id}&cate_name={cate_name}')

def delete_quantity(request,item_name):
     table_id=request.GET.get('table_no')
     cate_name=request.GET.get('cate_name')
     cart=cart_items.objects.filter(Table_id__Table_id=table_id)
     for cart_item in cart:
         if cart_item.item_name==item_name:
             if cart_item.quantity==1:
                 cart_item.delete()
                 return redirect(f'/staffside/pos/?table_no={table_id}&cate_name={cate_name}')
             else:
                 cart_item.quantity-=1
                 cart_item.save()
                 return redirect(f'/staffside/pos/?table_no={table_id}&cate_name={cate_name}')
    
     return redirect(f'/staffside/pos/?table_no={table_id}&cate_name={cate_name}')




@login_required(login_url='/staffside/')
def sales(request):  
    timezone.activate('Asia/kolkata')
    today=timezone.now().date()

    sales_data=Sales_details.objects.all()
    sales_data1=Sales_details.objects.filter(staff_name=request.user.first_name).order_by('-timeanddate')
    total_sales=Sales_details.objects.values_list('total_amount',flat=True)
    total_orders=Sales_details.objects.values_list('order_id',flat=True)
    total_sales=sum(total_sales)
    total_orders=len(total_orders)
    total_quantites=Sales_Report.objects.values('item_name').annotate(quantity=Sum('quantity'))
    max_quantity=total_quantites.aggregate(Max('quantity'))['quantity__max']
    print(max_quantity,'-----------------')
    best_selling_items=total_quantites.values('item_name').filter(quantity=max_quantity)
    print(best_selling_items,'-----------------')  
  
    total_revenue_today=Sales_details.objects.filter(timeanddate__date=today,staff_name=request.user.first_name).aggregate(Sum('total_amount'))['total_amount__sum']
    total_orders_today=Sales_details.objects.filter(timeanddate__date=today,staff_name=request.user.first_name).aggregate(Count('order_id'))['order_id__count']                            
    
    context={
        'sales_data':sales_data,
        'sales_data1':sales_data1,
        'total_sales':total_sales,
        'total_orders':total_orders,
        'best_selling_items':best_selling_items,
        'total_revenue_today':total_revenue_today,
        'total_orders_today':total_orders_today
    }

    return render_page(request, 'staffside/sales.html',context)

@login_required(login_url='/staffside/')
def customer(request):
    timezone.activate('Asia/Kolkata')
    customers = Customer.objects.all().order_by('-id')
    form = CustomerForm()
 
    if request.method=='POST':
        form=CustomerForm(request.POST)
        if form.is_valid():
          form.save()
          return redirect('/staffside/customer')
        else:
            messages.error(request,'There is an error in any field,check below')


    context={
        'customers': customers, 
        'form': form
    }

    return render_page(request, 'staffside/customer.html', context)

def update_customer(request):
        timezone.activate('Asia/Kolkata')
        if request.method == 'POST':
            customer_id = request.POST.get('customer_id')
            customer = Customer.objects.get(id=customer_id)
            form = CustomerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                messages.success(request, "Updated successfully.")
                return redirect('/staffside/customer/')

            else:
                print(form.errors,'------------------------')
                messages.error(request, "Invalid data.")
                return redirect('/staffside/customer/')

def delete_customer(request):
    timezone.activate('Asia/Kolkata')
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')   
        customer = Customer.objects.filter(id=customer_id).first()
        if customer:
            customer.delete()
            messages.success(request, "Purchase deleted successfully.")
        else:
           pass
    return redirect('/staffside/customer/')

def staffside_settings_view(request):
    return redirect('staffside:profile')

@login_required(login_url='/staffside/')
def render_settings_page(request, template, context=None):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, template, context or {})
    context = context or {}
    context["template"] = template  # Ensures `template` is still passed
    return render(request, "staffside/settings.html", context)

@login_required(login_url='/staffside/')
def change_password(request):
    current_user=request.user
    form = UpatePasswordForm(user=current_user)
    if request.method=='POST':
       form=UpatePasswordForm(user=current_user,data=request.POST)
       if form.is_valid():
           form.save()
           update_session_auth_hash(request,form.user)
           messages.success(request,('Password have been changed successfully'))
           return redirect('/staffside/change_password/')
       else:
          messages.error(request,('Please correct the errors below'))
          print(form.errors,'-------------------------')
    
     
    context={
        "form":form
    }  
    return render_settings_page(request, "staffside/settings/change_password.html", context)


def edit_profile(request):
    return render_settings_page(request,"staffside/settings/edit_profile.html")

@login_required(login_url='/staffside/')
def profile(request):
    timezone.activate('Asia/Kolkata')
    user_form=UpdateUserForm(request.user)

    if request.user.is_authenticated:
        current_user=CustomUser.objects.get(id=request.user.id)
        user_form=UpdateUserForm(request.POST or None,instance=current_user)
        if user_form.is_valid():
             user_form.save()
             messages.success(request,'User details have  been  Updated  successfully')
             return redirect('/staffside/profile/')
    context={
        "user_form":user_form
    }
    return render_settings_page(request,"staffside/settings/profile.html",context)

def save_image(request,id):
    if request.method=="POST" and request.FILES :
        image=request.FILES.get('image')
        current_user=CustomUser.objects.get(id=id)
        current_user.image=image
        current_user.save()
        messages.success(request,'Image is uploaded successfully')
        return redirect('/staffside/profile/')

    
    

def logout_view(request):
    return render_page(request, 'staffside/logout.html')

def logout_user(request):
    logout(request)
    return redirect('staffside:login')
