from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path("", views.index,  name="shopHome"),
    path("about/", views.about,      name="about us"),
    path("contact/", views.contact,      name="contact us"),
    path("search/", views.search,      name="search"),
    path("productview/<int:myid>", views.prodview,        name="ProductView"),
    path("order/<int:myid>", views.order,     name="checkout"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name = 'sellproduct.html'),        name = 'home'),
    path('social-auth/', include('social_django.urls',       namespace='social')),
    path('success/', views.success,      name='success'),
    path('success1/', views.success1,      name='success1'),
    path('success2/', views.success2,      name='success2'),
    path('sellproduct/', views.sellproduct,      name='sellproduct' ),
    path('view/', views.show_file,       name="view"),
    path('profile/', views.profile,       name="profile"),
    path('vieworder/', views.vieworder,       name="vieworder"),
    path('orderrequest/', views.orderrequest,       name="orderrequest"),
    path('yourproduct/', views.yourproduct,       name="yourproduct"),
    path('delete/<int:myid>', views.delete,       name="profile"),
]