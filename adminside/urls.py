from django.urls import path
from . import views

app_name = "adminside"

urlpatterns = [
    # path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('branches/', views.branches, name='branches'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('purchase/', views.purchase, name='purchase'),
    path('categories/', views.categories, name='categories'),
    path('inventory/', views.inventory, name='inventory'),
    path('fooditems/', views.fooditems, name='fooditems'),
    path('customer/', views.customer, name='customer'),
    path('staff/', views.staff, name='staff'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.adminside_settings_view, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
    path('branches/update/', views.update_branch, name='update_branch'),
    path('branches/delete/', views.delete_branch, name='delete_branch'),
    path('staff/delete/',views.delete_staff,name='delete_staff'),
    path('login/',views.login_view,name='login'),
    path('categories/update/',views.update_category,name='update_category'),
    path('categories/delete/',views.delete_category,name='delete_category'),
    path('inventory/update/',views.update_inventory,name='update_inventory'),
    path('get_update_form/<int:id>/',views.get_update_form,name='get_update_form')
]
