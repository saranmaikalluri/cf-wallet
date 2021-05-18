import os
from functools import partial, reduce
import operator
import datetime
import calendar
import wallet
from django.shortcuts import render
from django.db.models import Sum, Q
from django.views.decorators.csrf import csrf_exempt
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
from main.models import Aspnetusers, Student,Universities,Courses,Acknowledgements,Aspnetuserroles
from twilio.rest import Client
from django.conf import settings
from .otp_funcs import send_otp,verify_otp
from .paginations import CursorSetPagination, StandardResultsSetPagination
from twilio.base.exceptions import TwilioRestException
from main.serializers import AspNetUserSerializer
from django.db import connection
from django.http import JsonResponse


@api_view(['GET','PUT'])
def wallet_detail(request):
    user= request.GET.get('user')
    try:
        wallet_data= Wallet.objects.get(user=str(user))
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   
    if request.method=='GET':
        serializer= WalletSerializer(wallet_data)
        return Response(serializer.data)
    elif request.method=='PUT':
        wallet_data= Wallet.objects.get(user=user)
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
    

@api_view(['GET'])
def user_transactions_list(request):
    # wallet_id= request.GET.get('wallet_id')
    wallet_id= request.data['wallet_id']
    print(wallet_id)
    try:
        transactions_data= WalletTransactions.objects.filter(wallet=wallet_id)
        print(transactions_data)
        serializer= TransactionsSerializer(transactions_data,many=True)
        return Response(serializer.data)
    except WalletTransactions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

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




class TransactionsViewSet(viewsets.ModelViewSet):
    serializer_class=TransactionsSerializer
    pagination_class=StandardResultsSetPagination
    def get_queryset(self):
        transactions = transaction_search(self.request)
        return transactions.order_by('-transaction_date')

@api_view(['POST'])
def send_otp_to_user(request):
    # mobile_no=request.data['mobile_no']
    partner_id= request.data['partner_id']
    amount= request.data['amount']
    partner_data= Aspnetusers.objects.get(id= partner_id)
    partner_name= partner_data.username
    if int(amount)<=int(10000):
        user_data= WalletOTPAdmin.objects.get(transaction_limit=int(10000))
        user_mobile= user_data.mobile_no
        user_mobile='+91'+str(user_mobile)
        print(user_mobile)
        try:
            send_otp(user_mobile)
            return Response({'message':f'OTP sent successfully for initiating transaction of {partner_name}','status':status.HTTP_200_OK})
        except Exception as e:
            print(str(e))
            return Response({'message':str(e),'status':status.HTTP_400_BAD_REQUEST})
    if int(amount)>int(10000):
        user_data= WalletOTPAdmin.objects.get(transaction_limit=int(1000000))
        user_mobile= user_data.mobile_no
        user_mobile='+91'+str(user_mobile)
        print(user_mobile)
        try:
            send_otp(user_mobile)
            return Response({'message':f'OTP sent successfully for initiating transaction of {partner_name} ','status':status.HTTP_200_OK})
        except Exception as e:
            print(str(e))
            return Response({'message':str(e),'status':status.HTTP_400_BAD_REQUEST})

    
@api_view(['POST'])
def verify_user_otp(request):
    mobile_no=request.data['mobile_no']
    otp= request.data['otp']
    partner_id= request.data['partner_id']
    staff_id= request.data['staff_id']
    transaction_amount= request.data['amount']
    partner_wallet= Wallet.objects.get(user=str(partner_id))
    partner_balance= partner_wallet.balance
    partner_data= Aspnetusers.objects.get(id= partner_id)
    partner_name= partner_data.username
    try:
        data= verify_otp(mobile_no,otp)  
        if data=='approved':
            partner_wallet.deposit(int(transaction_amount))
            transaction_data= WalletTransactions.objects.create(wallet=partner_wallet,transaction_amount=transaction_amount,balance=partner_balance)
            transaction_data.save()
            staff_transaction= StaffPartnerTransactions.objects.create(wallet_transaction_id=transaction_data,staff_id=staff_id,partner_id=partner_id)
            staff_transaction.save()
            return Response({'message':f'OTP verified successfully and amount credited to {partner_name}','status':status.HTTP_200_OK})
        else:
            return Response({'message':'Unable to verify OTP. Please try again','status':status.HTTP_400_BAD_REQUEST})
    except Exception as e:
        print(str(e))
        return Response({'message':str(e),'status':status.HTTP_400_BAD_REQUEST})




@api_view(['GET'])
def get_partners(request):
    cursor= connection.cursor()
    cursor.execute("select a.Id, a.UserName, a.Email from AspNetUsers a join AspNetUserRoles r on a.Id = r.UserId and r.RoleId=7")
    data= cursor.fetchall()
    res=[{'id':i[0],'username':i[1],'email':i[2]} for i in data]
    print(data)
    try:
        query= request.data['query']
        if len(query)>=3:
            filters = dict(map(res['email'],query))
            qs=res.filter(**filters)
            print(qs)
        return JsonResponse(res, status=status.HTTP_200_OK,safe=False)
    except Exception as e:
        return JsonResponse({'message':str(e),'status':status.HTTP_400_BAD_REQUEST})