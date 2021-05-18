from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

  

def send_otp(mobile):
    account_sid= settings.TWILIO_ACCOUNT_SID
    auth_token= settings.TWILIO_AUTH_TOKEN
    twilio_client= Client(account_sid,auth_token)
    VERIFY_SERVICE_SID= settings.TWILIO_SERVICE_ID
    print(account_sid)   
    twilio_client.verify.services(VERIFY_SERVICE_SID).verifications.create(to=mobile, channel='sms',locale='en')

def verify_otp(mobile, otp):
    account_sid= settings.TWILIO_ACCOUNT_SID
    auth_token= settings.TWILIO_AUTH_TOKEN
    twilio_client= Client(account_sid,auth_token)
    VERIFY_SERVICE_SID= settings.TWILIO_SERVICE_ID
    check = twilio_client.verify.services(VERIFY_SERVICE_SID).verification_checks.create(to=mobile,code=otp)
    print(check.status)
    return check.status