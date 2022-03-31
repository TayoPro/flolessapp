from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('products', views.products, name='products'),
    path('product/<str:id>/<slug:slug>', views.product, name='product'),
    path('detail/<str:id>/<slug:slug>', views.detail, name='detail'), 
    path('accountform/',  views.accountform, name='accountform'),
    path('login/',  views.loginform, name='loginform'),
    path('logout/',  views.logoutfunc, name='logoutfunc'),
    path('register/',  views.registerform, name='registerform'),
    path('training/', views.training, name='training'),
    path('profile/', views.userprofile, name='userprofile'),
    path('confirm/', views.confirm, name='confirm'),
    path('update/', views.userupdate, name='userupdate'),
    path('password/', views.userpassword, name='userpassword'),
    path('addtoshopcart/', views.addtoshopcart, name='addtoshopcart'),
    path('shopcart/', views.shopcart, name='shopcart'),
    path('updatequantity/',views.updatequantity,name='updatequantity'),
    path('deletefromcart/<str:id>', views.deletefromcart, name='deletefromcart'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('placeorder/', views.placeorder, name ='placeorder'),
    path('payfee/', views.payfee, name ='payfee'),
    path('ordercompleted/', views.ordercompleted, name='ordercompleted'),
]