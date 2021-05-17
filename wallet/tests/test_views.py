import json
from django.test import TestCase,Client
from django.urls import reverse
from rest_framework import status
from wallet.models import Wallet
from wallet.serializers import WalletSerializer
from django.contrib.auth.models import User

client=Client()

class GetUserWalletInfo(TestCase):
    """Test Module to get wallet information of a user"""
    def setUp(self):
        u1= User.objects.create_user(username='admin1', password='Admin#12345')
        u2= User.objects.create_user(username='admin2', password='Admin#12345')
        u3= User.objects.create_user(username='admin3', password='Admin#12345')
        u4= User.objects.create_user(username='admin4', password='Admin#12345')
        w1=Wallet.objects.create(user=u1,balance=1000)
        w2=Wallet.objects.create(user=u2,balance=2000)
        w3=Wallet.objects.create(user=u3,balance=3000)
        w4=Wallet.objects.create(user=u4,balance=4000)
    def test_user_data(self):
        u2= User.objects.create_user(username='admin6', password='Admin#12345')
        w2=Wallet.objects.create(user=u2,balance=2000)
        response= client.get(reverse('wallet_detail',kwargs={'pk':w2.pk}))
        print(response)
        w= Wallet.objects.get(pk=w2.pk)
        serializer= WalletSerializer(w)
        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code,status.status.HTTP_200_OK)
    def test_invalid_data(self):
        response= client.get(reverse('get_delete_update_wallet',kwargs={'pk':6}))
        self.assertEqual(response.status_code,status.status.HTTP_200_OK)

