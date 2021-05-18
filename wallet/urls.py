from django.urls import path,include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
# from wallet.views import TransactionsViewSet
from . import views

router= DefaultRouter()
router.register(r'transactions',views.TransactionsViewSet,basename='transactions')

urlpatterns=[ 
  url('wallet/$', views.wallet_detail, name='wallet_detail'),
  url('transfers/send_otp',views.send_otp_to_user,name='send_otp_to_user'),
  url('transfers/verify_otp',views.verify_user_otp,name='verify_user_otp'),
  url('partners/get_partners',views.get_partners,name='get_partners')

]

urlpatterns += [
  url(r'',include(router.urls))
  ]