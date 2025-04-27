from django.urls import path
from . import views
from adminside.views import login_view
app_name = "staffside"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('orders/', views.orders, name='orders'),
    path('tables/', views.tables, name='tables'),
    path('pos/', views.pos, name='pos'),
    path('sales/', views.sales, name='sales'),
    path('customer/', views.customer, name='customer'),
    path('customers/update/', views.update_customer, name='update_customer'),
    path('customers/delete/', views.delete_customer, name='delete_customer'),
    path('settings/', views.staffside_settings_view, name='settings'),
    path('profile/', views.profile, name='profile'),
    # path('profile/change_profile_details',views.change_profile_details,name='change_profile_details'),
    path('edit_profile/save_image/<int:id>/',views.save_image,name='save_image'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
    path('logoutuser/',views.logout_user,name='logoutuser'),
    path('pos/cart/',views.cart,name='cart'),
    # path('filter_table/<int:id>/',views.table_filter,name='filter_table')
    path('pos/add_quantity/<str:item_name>/',views.add_quantity,name='add_quantity'),
    path('pos/delete_quantity/<str:item_name>/',views.delete_quantity,name='delete_quantity'),
    path('pos/order/',views.orders_taken,name='orders_taken'),
    path('order/save_changed_order/',views.save_changed_order,name='save_changed_order'),
    path('orders/cancel_order/',views.cancel_order,name='cancel_order'),
    path('pos/payment/',views.payment_page,name='payment_page'),
    path('pos/payment/payment_method/',views.confirm_payment,name='payment_method'),
    path('pos/payment/payment_method/final_payment',views.final_payment,name='final_payment'),
    path('pos/payemnt/payment_method/final_payment/final_exit/',views.final_exit,name='final_exit'),
    path('',login_view,name='login')
]
