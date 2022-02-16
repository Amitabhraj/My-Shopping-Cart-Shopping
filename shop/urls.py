from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path("", views.index,  name="shopHome"),
    path("register/", views.register,  name="register"),
    path("login/", views.login_page,  name="login_page"),
    path("verify_otp/", views.verify_otp,  name="verify_otp"),
    path("starter/", views.starter,  name="starter"),
    path("dashboard/", views.dashboard,  name="dashboard"),
    path("handlerequest/", views.handlerequest,      name="handlerequest"),
    path("about/", views.about,      name="about us"),
    path("contact/", views.contact,      name="contact us"),
    path("search/", views.search,      name="search"),
    path("productview/<int:myid>", views.prodview,        name="ProductView"),
    path("order/<int:myid>", views.order,     name="order"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name = 'sellproduct.html'),        name = 'home'),
    path('social-auth/', include('social_django.urls',       namespace='social')),
    path('sellproduct/', views.sellproduct,      name='sellproduct' ),
    path('view/', views.show_file,       name="view"),
    path('profile/', views.profile,       name="profile"),
    path('vieworder/', views.vieworder,       name="vieworder"),
    path('cart/', views.cart,       name="cart"),
    path('cart/cart_delete/<int:myid>', views.cart_delete,       name="cart_delete"),
    path('orderrequest/', views.orderrequest,       name="orderrequest"),
    path('moredetail/<int:myid>', views.moredetail,       name="moredetail"),
    path('moredetail/update2/<int:myid>', views.update2,      name="update2"),
    path('yourproduct/', views.yourproduct,       name="yourproduct"),
    path('vieworder/destroy/<int:myid>', views.destroy,       name="destroy"),
    path('edit/delete/<int:myid>', views.delete,       name="delete"),
    path('edit/<int:myid>', views.edit, name='edit'),
    path('edit/update/<int:myid>', views.update, name='update'), 
    path('seller/contactus/', views.seller_contact, name='seller-contact'), 
    path('success/', views.success, name='success'), 
]
