import os
from functools import partial, reduce
import operator
import datetime
import calendar
from django.shortcuts import render
from django.db.models import Sum, Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, response
import rest_framework
from rest_framework import serializers
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters,status,viewsets,generics
from wallet.serializers import WalletSerializer,TransactionsSerializer
from wallet.models import Wallet,WalletTransactions,StaffPartnerTransactions,WalletEmailAdmin,WalletOTPAdmin
from wallet.helpers import prev_month_range,prev_year_range
from django.shortcuts import get_object_or_404
from rest_framework.pagination import CursorPagination
from core.models import Student,Universities,Courses,Acknowledgements,Aspnetuserroles
from twilio.rest import Client
from django.conf import settings
from .otp_funcs import send_otp,verify_otp
from twilio.base.exceptions import TwilioRestException


@api_view(['GET','PUT'])
def wallet_detail(request):
    user_id= request.GET.get('user_id')
    try:
        wallet_data= Wallet.objects.get(user=user_id)
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   
    if request.method=='GET':
        serializer= WalletSerializer(wallet_data)
        return Response(serializer.data)
    elif request.method=='PUT':
        wallet_data= Wallet.objects.get(user=user_id)
        balance= request.data['balance']
        print(balance)
        serializer = WalletSerializer(wallet_data, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            td=serializer.data
            WalletTransactions.objects.get_or_create(wallet=wallet_data,transaction_date=td['updated_on'],
                    transaction_amount=balance,balance=td['balance'])
                
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
def transaction_search(request):
    user = request.GET.get('user')
    wallet = request.GET.get('wallet')
    string = request.GET.get('string')
    application_id = request.GET.get('application_id')
    transaction_amount = request.GET.get('transaction_amount')
    transaction_status = request.GET.get('transaction_status')
    transaction_date = request.GET.get('transaction_date')
    transactions= WalletTransactions.objects.all().order_by('-transaction_date')
    if user:
        transactions = WalletTransactions.objects.filter(wallet__user=user)
        print(transactions)

    if wallet:
        transactions = WalletTransactions.objects.filter(wallet=wallet)

    if string:
        # search multiple terms
        if ',' in string:
            string = [s.strip() for s in string.split(',')]            
            application = reduce(operator.or_, (Q(transaction__application__name__icontains = s) for s in string))
            transactions = transactions.filter(application | transaction_amount | transaction_status)
        else:      
            transactions = transactions.filter(Q(transaction__comments__icontains = string) | Q(transaction__status__icontains = string))

    if application_id:
        application_id = application_id.split(',')
        transactions = transactions.filter(item__application__id__in = application_id)

    if transaction_amount:
        transactions = transactions.filter(transaction_amount__eq = transaction_amount)

    if transaction_date:
        if 'range' in transaction_date:
            date = transaction_date.split('.')
            date[0] = date[0].replace('range', '')
            transactions = transactions.filter(transaction__date__range = date)
        
        elif transaction_date == 'prev_year':
        
            prev_year = prev_year_range()
            transactions = transactions.filter(date__range = [prev_year['start'], prev_year['end']])
        
        elif transaction_date == 'prev_month':
        
            prev_month = prev_month_range()
            transactions = transactions.filter(date__range = [prev_month['start'], prev_month['end']])
        
        elif transaction_date == 'current_year':
        
            today = datetime.datetime.today()
            last_date = datetime.date(today.year, 12, 31)
            first_date = datetime.date(today.year, 1, 1)            
            transactions = transactions.filter(date__range = [first_date, last_date])        
        
        elif transaction_date == 'current_month':
        
            today = datetime.datetime.today()
            last_date = calendar.monthrange(today.year, today.month)[1]
            last_date = datetime.date(today.year, today.month, last_date)
            first_date = datetime.date(today.year, today.month, 1)

            transactions = transactions.filter(date__range = [first_date, last_date])

    return transactions




@api_view(['GET'])
def transactions_list(request):
    wallet_id= request.GET.get('wallet_id')
    print(wallet_id)
    try:
        transactions_data= WalletTransactions.objects.filter(wallet=wallet_id)
        print(transactions_data)
        serializer= TransactionsSerializer(transactions_data,many=True)
        return Response(serializer.data)
    except WalletTransactions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_transaction(request):
    wallet_id= request.data['wallet_id']
    student_id= request.data['student_id']
    ack_id= request.data['ack_id']
    university_id= request.data['university_id']
    course_id= request.data['course_id']
    transaction_amount= request.data['transaction_amount']
    currency= request.data['currency']
    markup_fee= request.data['markup_fee']
    exchange_rate= request.data['exchange_rate']
    exchange_amount= request.data['exchange_amount']
    couponcode= request.data['couponcode']
    user_id=request.data['user_id']
    try:
        wallet_data=Wallet.objects.get(pk=wallet_id)
        student_data=Student.objects.get(pk=student_id)
        application_data=Acknowledgements.objects.get(pk=ack_id)
        university_data= Universities.objects.get(pk=university_id)
        course_data=Courses.objects.get(pk=course_id)
        user_data= User.objects.get(pk=user_id)
        wallet_balance=wallet_data.balance
        if wallet_data.valid_withdraw_amount(transaction_amount)==True:
            print("yes")
            transaction_balance=float(wallet_balance)-float(transaction_amount)
            print(transaction_balance)
            transaction_data= WalletTransactions.objects.create(wallet=wallet_data,transaction_amount=transaction_amount,balance=transaction_balance)
            print("data is",transaction_data)
            transaction_data.save()
            # transaction_details= TransactionDetail.objects.create(transaction=transaction_data,student=student_data,
            #                         application=application_data,course=course_data, university=university_data,
            #                         currency=currency,markup_fee=markup_fee,exchange_rate=exchange_rate,exchange_amount=exchange_amount,couponcode=couponcode,staff_id=user_data)
            # transaction_details.save()
            # serializer= TransactionDetailsSerializer(transaction_details)
            # if serializer.is_valid():
                # serializer.save()
            # return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        # return Response(serializer.errors,
                        # status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message':str(e),
                        'status':status.HTTP_400_BAD_REQUEST})


@api_view(['POST','PUT'])
def send_money_to_partner(request):
    staff_id= request.data['staff_id']
    partner_id= request.data['partner_id']
    amount= request.data['amount']
    remarks=request.data['remarks']
    if float(amount)<=float(10000):
        otp_user= WalletOTPAdmin.objects.get(transaction_limit=int(10000))
        opt_mobile_no= otp_user.mobile_no
        print("yes")
        partner_wallet= Wallet.objects.get(user=partner_id)
        print(partner_wallet)
        partner_balance= partner_wallet.deposit(int(amount))
        print(partner_wallet)
        serializer = WalletSerializer(partner_wallet)
        print(serializer.data)
        td=serializer.data
        transaction_data= WalletTransactions.objects.create(wallet=partner_wallet,transaction_date=td['updated_on'],
                  transaction_amount=amount,balance=td['balance'],remarks=remarks) 
        transaction_data.save() 
        serializer= TransactionsSerializer(transaction_data)                  
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    return Response({'message':'Requested transaction amount is greater than the allocated limit', 'status':status.HTTP_401_UNAUTHORIZED})


# @api_view(['POST'])
# def close_partner_account(request):
#     staff_id= request.data['staff_id']
#     partner_id= request.data['partner_id']
#     remarks=request.data['remarks']
#     staff_role= UserRoles.objects.get(user=staff_id)
#     st_role= staff_role.role.name
#     if st_role=='staff':
#         partner_wallet= Wallet.objects.get(user=partner_id)
#         closing_balance=partner_wallet.balance
#         print(closing_balance)
#         partner_wallet.empty_wallet_balance()
#         serializer= WalletSerializer(partner_wallet)
#         td=serializer.data
#         if int(closing_balance)>int(0):
#             transaction_data= WalletTransactions.objects.create(wallet=partner_wallet,transaction_date=td['updated_on'],
#                   transaction_amount=closing_balance,balance=0,remarks=remarks) 
#             transaction_data.save() 
#             serializer= TransactionsSerializer(transaction_data)   
#             print(serializer.data)        
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'message':'Partner wallet is empty','status':status.HTTP_204_NO_CONTENT})      
#     else:
#         return Response({'message':'Invalid request','status':status.HTTP_401_UNAUTHORIZED})

class CursorSetPagination(CursorPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    ordering = '-transaction_date'

class TransactionsViewSet(viewsets.ModelViewSet):
    serializer_class=TransactionsSerializer
    pagination_class=CursorSetPagination
    def get_queryset(self):
        transactions = transaction_search(self.request)
        return transactions.order_by('-transaction_date')

@api_view(['POST'])
def send_otp_to_user(request):
    mobile_no=request.data['mobile_no']  
    try:
        send_otp(mobile_no)
        return Response({'message':'OTP sent successfully','status':status.HTTP_200_OK})
    except Exception as e:
        print(str(e))
        return Response({'message':str(e),'status':status.HTTP_400_BAD_REQUEST})
    
@api_view(['POST'])
def verify_user_otp(request):
    mobile_no=request.data['mobile_no']
    otp= request.data['otp']
    try:
        data= verify_otp(mobile_no,otp)  
        if data=='approved':
            return Response({'message':'OTP verified successfully','status':status.HTTP_200_OK})
        else:
            return Response({'message':'Unable to verify OTP. Please try again','status':status.HTTP_400_BAD_REQUEST})
    except Exception as e:
        print(str(e))
        return Response({'message':str(e),'status':status.HTTP_400_BAD_REQUEST})
