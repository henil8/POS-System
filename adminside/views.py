from django.shortcuts import render, redirect,get_object_or_404
from .forms import CustomPasswordChangeForm,StaffRegisterForm,InventoryForm
from .models import Branch,Inventory,Purchase,CustomUser,Categories
from django.contrib.auth.forms import UserChangeForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse


def home(request):
    return redirect('adminside:dashboard')

def render_page(request, template, data=None):
    if data is None:
        data={}
    return render(request, "adminside/base.html", {"template": template, "data":data})

def dashboard(request):
    return render_page(request, 'adminside/dashboard.html')




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

def suppliers(request):
    return render_page(request, 'adminside/suppliers.html')

def purchase(request):    
    return render_page(request, 'adminside/purchase.html')

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



def inventory(request):
    form=InventoryForm()
    if request.method=='POST':
        form=InventoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/adminside/inventory/')
        else:
            messages.error(request,"Invalid Details")
    
    inventory=Inventory.objects.all()
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

def fooditems(request): 
    return render_page(request, 'adminside/fooditems.html')

def customer(request):
    return render_page(request, 'adminside/customer.html')

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
            
    staffs=CustomUser.objects.all() 
    context={
        "form":form,
        "staffs":staffs
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


def reports(request):
    sales_data = [
    {"product_id": "101", "product_name": "Neapolitan Pizaa", "calegories": "Pizaa", "email": "john.doe@example.com", "quentity": "450", "paid": "200", "balance": "250", "date": "01/15"},
    {"product_id": "102", "product_name": "Veg. Burger", "calegories": "Burger", "email": "jane.smith@example.com", "quentity": "350", "paid": "150", "balance": "200", "date": "01/16"},
    {"product_id": "103", "product_name": "French Fries", "calegories": "Fast Food", "email": "robert.brown@example.com", "quentity": "500", "paid": "250", "balance": "250", "date": "01/17"},
    {"product_id": "104", "product_name": "Veg. Sandvich", "calegories": "Sandvich", "email": "emily.white@example.com", "quentity": "600", "paid": "300", "balance": "300", "date": "01/18"},
    {"product_id": "105", "product_name": "Dosa (Butter)", "calegories": "South Indian", "email": "michael.green@example.com", "quentity": "750", "paid": "500", "balance": "250", "date": "01/19"},
    ]
    return render_page(request, 'adminside/reports.html', data=sales_data)


def adminside_settings_view(request):
    return redirect('adminside:profile')

def render_settings_page(request, template, context=None):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, template, context or {})
    context = context or {}
    context["template"] = template  # Ensures `template` is still passed
    return render(request, "adminside/settings.html", context)

def change_password(request):
    form = CustomPasswordChangeForm(request.user)
    return render_settings_page(request, "adminside/settings/change_password.html", {'form': form})

def edit_profile(request):
    return render_settings_page(request,"adminside/settings/edit_profile.html")

def profile(request):
    return render_settings_page(request,"adminside/settings/profile.html")

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
                 
            #    login(request,user)
              
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