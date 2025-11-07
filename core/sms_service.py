import os
from django.conf import settings

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    Client = None


def send_otp_sms(mobile_number, otp, user_type='user'):
    if not TWILIO_AVAILABLE:
        print("Twilio library not installed. Please install: pip install twilio")
        return False
    
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        twilio_phone = os.getenv('TWILIO_PHONE_NUMBER', '')
        
        if not account_sid or not auth_token or not twilio_phone:
            print("Twilio credentials not configured in environment variables")
            return False
        
        client = Client(account_sid, auth_token)
        
        if not mobile_number.startswith('+'):
            if mobile_number.startswith('0'):
                mobile_number = '+91' + mobile_number[1:]
            elif len(mobile_number) == 10:
                mobile_number = '+91' + mobile_number
            else:
                mobile_number = '+' + mobile_number
        
        user_label = "Admin" if user_type == 'admin' else "Donor"
        
        message_body = f"""Your BrightFutures password reset OTP is {otp}. This OTP is valid for 10 minutes. Do not share this OTP with anyone."""
        
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone,
            to=mobile_number
        )
        
        print(f"SMS sent successfully. SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

