from django.urls import path
from . import views
#for loading images
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name='home'),
    path('products/',views.products,name='products'),
    path('customer/<str:pk_test>',views.customer,name='customer'),

    path('accounts',views.accounts_settings,name='accounts-settings'),

    #CRUD
    path('create_order/<int:pk>/',views.createOrder,name='create-order'),
    path('update_order/<int:pk>/',views.updateOrder,name='update-order'),
    path('delete_order/<int:pk>/',views.deleteOrder,name='delete-order'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)