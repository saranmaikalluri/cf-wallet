from django.test import TestCase
from wallet.models import Wallet,Transaction,Student,Application,Course,University
from django.contrib.auth.models import User


class WalletTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='admin1', password='Admin#12345')
        user1.save()
        user2=User.objects.create_user(username='admin2', password='Admin#12345')
        user2.save()
        Wallet.objects.create(user=user1,balance=1000)
        Wallet.objects.create(user=user2,balance=30000)
    def test_user_wallet(self):
        user1 = User.objects.create_user(username='admin3', password='Admin#12345')
        user1.save()
        user2=User.objects.create_user(username='admin4', password='Admin#12345')
        user2.save()
        u1= Wallet.objects.get(user=1)
        u2=Wallet.objects.get(user=2)
        self.assertEqual(u1.get_wallet_data(),'1000.0000')
        self.assertEqual(u2.get_wallet_data(),'30000.0000')
       