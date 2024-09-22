"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from web.views import account, level, customer, policy, my_order, my_transaction, my_space

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('/', account.index, name='index'),

    path('login/', account.login, name='login'),
    path('logout/', account.logout, name='logout'),
    path('sms_send/', account.sms_send, name='sms_send'),

    path('home/', account.home, name='home'),

    path('level/', level.level, name='level'),
    path('level/add/', level.level_add, name='level_add'),
    path('level/edit/<int:pk>/', level.level_edit, name='level_edit'),
    path('level/delete/', level.level_delete, name='level_delete'),

    path('customer/', customer.customer, name='customer'),
    path('customer/add/', customer.customer_add, name="customer_add"),
    path('customer/edit/<int:pk>/', customer.customer_edit, name="customer_edit"),
    path('customer/reset/<int:pk>/', customer.customer_reset, name="customer_reset"),
    path('customer/delete/', customer.customer_delete, name="customer_delete"),
    path('customer/charge/<int:pk>/', customer.customer_change, name="customer_change"),
    path('customer/add_charge/<int:pk>/', customer.customer_add_change, name="customer_add_change"),

    path('policy/', policy.policy, name="policy"),
    path('policy/add/', policy.policy_add, name="policy_add"),
    path('policy/edit/<int:pk>/', policy.policy_edit, name="policy_edit"),
    path('policy/delete/', policy.policy_delete, name="policy_delete"),

    path('my_order/', my_order.my_order, name="my_order"),
    path('my_order/add/', my_order.my_order_add, name="my_order_add"),
    path('my_order/cancel/<int:pk>/', my_order.my_order_cancel, name="my_order_cancel"),

    path('my_transaction/', my_transaction.my_transaction, name="my_transaction"),
    path('transaction/', my_transaction.transaction, name="transaction"),

    path('my_space/', my_space.my_space, name='my_space')
]
