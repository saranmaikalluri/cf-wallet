from rest_framework import serializers
from .models import WalletOTPAdmin,WalletEmailAdmin
from .models import Wallet,WalletTransactions,RazorpayTransactions,StaffPartnerTransactions

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wallet
        fields=['balance','user']
    def update(self, instance, validated_data):
        balance= validated_data.get('balance')
        instance.balance= validated_data.get(instance.deposit(balance),instance.balance)
        return instance    

class RazorpayTransactionsSerializer(serializers.Serializer):
    class Meta:
        model=RazorpayTransactions
        fields='__all__'

class TransactionsSerializer(serializers.Serializer):
    id= serializers.IntegerField()
    # wallet= WalletSerializer(read_only=True)
    transaction_date= serializers.DateTimeField()
    transaction_amount= serializers.DecimalField(max_digits=18, decimal_places=4)
    balance= serializers.DecimalField(max_digits=18, decimal_places=4)
    remarks=serializers.CharField()
    updated_on=serializers.DateTimeField()
    transaction_status=serializers.CharField()

    class Meta:
        model=WalletTransactions
        fields=['id','transaction_date','transaction_amount','balance','remarks','updated_on','transaction_status']

# class TransactionDetailsSerializer(serializers.Serializer):
#     class Meta:
#         model= TransactionDetail
#         fields='__all__'

class WalletOTPAdminSerializer(serializers.Serializer):
    class Meta:
        model=WalletOTPAdmin
        fields='__all__'

class WalletEmailAdminSerializer(serializers.Serializer):
    class Meta:
        model=WalletEmailAdmin
        fields='__all__'

class StaffPartnerSerializer(serializers.Serializer):
    class Meta:
        model=StaffPartnerTransactions
        fields='__all__'