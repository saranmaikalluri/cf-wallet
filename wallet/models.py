from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related
from django.utils.translation import ugettext as _
import datetime
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator, int_list_validator


# Create your models here.


class Wallet(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    user= models.CharField(max_length=128, db_column='UserId', verbose_name='User')
    balance= models.DecimalField(_('Balance'), max_digits=12, decimal_places=4, db_column='Balance')
    created_on= models.DateTimeField(auto_now_add=True, db_column='CreatedOn')
    updated_on=models.DateTimeField(auto_now=True,db_column='UpdatedOn')

    class Meta:
        db_table = 'Wallet'
        verbose_name_plural= 'Wallet'
        verbose_name= 'Wallet'

    def __str__(self):
        return str(self.balance)
    def __unicode__(self):
        return str(self.balance)

    def clean(self):
        wallet_data= Wallet.objects.filter(user= self.user).count()
        if wallet_data>1:
            raise ValidationError("Only 1 wallet can be created per user")
    def deposit(self, amount):
        self.balance += amount
        self.save()
    def withdraw(self,amount):
        if self.valid_withdraw_amount(amount):
            self.balance -= amount
            self.save()
        else:
            raise Exception("Not enough balance")
    def can_send(self, amount):
        if float(self.balance) - float(amount) >= 0:
            return True
        else:
            return False
    def valid_withdraw_amount(self, amount):
        if float(self.balance) >= float(amount):
            return True
        else:
            return False 
    def get_wallet_data(self):
        return str(self.balance)
    def empty_wallet_balance(self):
        self.balance=0
        self.save()

    
    
class WalletTransactions(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    wallet= models.ForeignKey(Wallet, on_delete=models.DO_NOTHING, db_column='WalletId')
    transaction_date= models.DateTimeField(auto_now_add=True,db_column='TransactionDate')
    transaction_amount= models.DecimalField(max_digits=18, decimal_places=4,db_column='TransactionAmount')
    balance= models.DecimalField(max_digits=18, decimal_places=4,db_column='Balance')
    remarks= models.CharField(max_length=255, blank=True, null=True,db_column='Remarks')
    updated_on= models.DateTimeField(auto_now=True,db_column='UpdatedOn')
    transaction_status= models.CharField(max_length=10, blank=True,null=True,db_column='TransactionStatus')
    # razorpay_id= models.ForeignKey(RazorPayTransactions, on_delete=models.PROTECT, blank=True,null=True)
    class Meta:
        db_table = 'WalletTransactions'
        verbose_name_plural= 'Wallet Transactions'
        verbose_name= 'Wallet Transactions'

    def __str__(self):
        return str(self.transaction_date)
    def __unicode__(self):
        return str(self.transaction_date)
    # def create_deposit_transaction(self,transaction_amount):
    #     Wallet.objects.deposit(self,transaction_amount)   
    # def create_withdraw_transaction(self,transaction_amount):
    #     Wallet.objects.withdraw(self,transaction_amount)

class RazorpayTransactions(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    order_id= models.CharField(max_length=255,blank=True,null=True, db_column='OrderId')
    payment_id= models.CharField(max_length=255, blank=True, null=True,db_column='PaymentId')
    amount= models.DecimalField(max_digits=18, decimal_places=4,db_column='Amount')
    email= models.EmailField(max_length=100, blank=False, null=False, db_column='Email')
    contact= models.CharField(max_length=10, blank=False, null=False,db_column='ContactNo')
    status= models.CharField(max_length=20, db_column='Status')
    payment_method= models.CharField(max_length=20, blank=True, null=True,db_column='PaymentMethod')
    wallet_transaction_id= models.ForeignKey(WalletTransactions,on_delete=models.DO_NOTHING,db_column='WalletTransactionId')
    created_on=models.DateTimeField(auto_now_add=True,db_column='CreatedOn')
    updated_on=models.DateTimeField(auto_now=True,db_column='UpdatedOn')

    def __str__(self):
        return self.id
    class Meta:
        db_table = 'RazorpayTransactions'
        verbose_name_plural= 'Razorpay Transactions'
        verbose_name= 'Razorpay Transactions'


class WalletOTPAdmin(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    mobile_no= models.CharField(max_length=10,validators=[int_list_validator(sep=''),MaxLengthValidator(10),], db_column='MobileNo')
    transaction_limit= models.IntegerField(db_column='TransactionLimit')
    created_on=models.DateTimeField(auto_now_add=True,db_column='CreatedOn')
    updated_on=models.DateTimeField(auto_now=True,db_column='UpdatedOn')
    def __str__(self) -> str:
        return str(self.mobile_no)
    def __unicode__(self) -> str:
        return str(self.mobile_no)
    class Meta:
        db_table = 'WalletOTPAdmin'
        verbose_name_plural= 'Wallet OTP Admin'
        verbose_name= 'Wallet OTP Admin'

class WalletEmailAdmin(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    email=models.EmailField(db_column='Email')
    created_on=models.DateTimeField(auto_now_add=True,db_column='CreatedOn')
    updated_on=models.DateTimeField(auto_now=True,db_column='UpdatedOn')
    def __str__(self) -> str:
        return str(self.email)
    def __unicode__(self) -> str:
        return str(self.email)
    class Meta:
        db_table = 'WalletEmailAdmin'
        verbose_name_plural= 'Wallet Email Admin'
        verbose_name= 'Wallet Email Admin'

class StaffPartnerTransactions(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    wallet_transaction_id= models.ForeignKey(WalletTransactions,on_delete=models.DO_NOTHING,db_column='WalletTransactionId')
    staff_id= models.CharField(max_length=128)
    partner_id= models.CharField(max_length=128)
    class Meta:
        db_table = 'StaffPartnerTransactions'
        verbose_name_plural= 'StaffPartnerTransactions'
        verbose_name= 'StaffPartnerTransaction'


# class TransactionDetail(models.Model):
    # transaction=models.ForeignKey(WalletTransaction,on_delete=models.DO_NOTHING)
    # student=models.ForeignKey('core.Student', on_delete=models.DO_NOTHING)
    # application= models.ForeignKey('core.Acknowledgements', on_delete=models.DO_NOTHING)
    # course= models.ForeignKey('core.Courses', on_delete=models.DO_NOTHING)
    # university=models.ForeignKey('core.Universities',on_delete=models.DO_NOTHING)
    # intake= models.CharField(max_length=10, blank=True,null=True)
    # year= models.CharField(max_length=4, blank=True, null=True)
    # exchange_rate= models.DecimalField(max_digits=18, decimal_places=4,blank=True, null=True)
    # markup_fee= models.DecimalField(max_digits=18, decimal_places=4,blank=True, null=True)
    # exchange_amount= models.DecimalField(max_digits=18, decimal_places=4)
    # currency=models.CharField(max_length=10, blank=True,null=True)
    # couponcode=models.CharField(max_length=10, blank=True,null=True)
    # discounted_amount= models.DecimalField(max_digits=18, decimal_places=4,blank=True, null=True)
    # staff_id=models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='staff_user1')
    # partner_id= models.ForeignKey(User, on_delete=models.DO_NOTHING,blank=True, null=True, related_name='partner_user1')

    # def __str__(self) -> str:
    #     return self.transaction
    # def __repr__(self) -> str:
    #     return self.transaction
    # def __unicode__(self):
    #     return self.transaction