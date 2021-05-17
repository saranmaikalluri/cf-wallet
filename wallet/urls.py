from django.urls import path,include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from wallet.views import TransactionsViewSet
from . import views

router= DefaultRouter()
router.register(r'transactions',TransactionsViewSet,basename='transactions')
# router.register(r'Users',views.UserViewSet, basename='users')
# router.register(r'wallet', views.WalletViewSet, basename='wallet')





urlpatterns=[
  url('wallet/(?P<id>[0-9]+)$', views.wallet_detail, name='wallet_detail'),
  # url('transactions/$',views.transactions_list,name='transactions_list'),
  # url('transactions',views.add_transaction, name='add_transaction'),
  url('send_money',views.send_money_to_partner,name='send_money_to_partner'),
  # url('close_partner_account',views.close_partner_account, name='close_partner_account'),
  url('send_otp_to_user',views.send_otp_to_user,name='send_otp_to_user'),
  url('verify_user_otp',views.verify_user_otp,name='verify_user_otp')
]

urlpatterns += [
	# url(r'^transactions-total/', TransactionsTotalViewSet.as_view(), name='transactions-total'),
  url(r'',include(router.urls))
  ]