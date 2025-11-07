import random
import os
from datetime import datetime, timedelta
from django.conf import settings

try:
    from .sms_service import send_otp_sms
    SMS_SERVICE_AVAILABLE = True
except ImportError:
    SMS_SERVICE_AVAILABLE = False
    send_otp_sms = None


def generate_otp():
    return f"{random.randint(0, 9999):04d}"


def send_otp_via_sms(mobile_number, otp, user_type='user'):
    try:
        if not SMS_SERVICE_AVAILABLE or not send_otp_sms:
            print("SMS service not available. Please install Twilio: pip install twilio")
            return False
        
        result = send_otp_sms(mobile_number, otp, user_type)
        return result
        
    except Exception as e:
        import traceback
        error_msg = f"Error sending OTP SMS: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return False


def is_otp_valid(otp_expiry_str):
    if not otp_expiry_str:
        return False
    
    try:
        expiry_time = datetime.fromisoformat(otp_expiry_str)
        return datetime.now() < expiry_time
    except (ValueError, TypeError):
        return False


def get_otp_expiry():
    return (datetime.now() + timedelta(minutes=10)).isoformat()

