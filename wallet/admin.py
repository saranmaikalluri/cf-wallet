from re import A
from django.contrib import admin
from wallet.models import RazorpayTransactions, WalletOTPAdmin,WalletEmailAdmin,WalletTransactions
from wallet.models import Wallet
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Wallet)
admin.site.register(WalletTransactions)
admin.site.register(WalletEmailAdmin)
admin.site.register(WalletOTPAdmin)