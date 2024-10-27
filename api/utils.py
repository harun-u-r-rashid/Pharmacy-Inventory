import random

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, EmailMessage
from user.models import User, OneTimePassword


def generateOtp():
        return ''.join(random.choices('1234567890', k=6))


def send_code_to_user(email):
        try:
                otp_code = generateOtp()
                user = User.objects.get(email=email)

                # Save the otp to the database

                otp_object = OneTimePassword.objects.create(user=user, code=otp_code)
                otp_object.save()


                # Email send

                email_subject = "Active your account"
                email_body = render_to_string('otp_email.html', {'otp_code':otp_code})

                email_message = EmailMultiAlternatives(email_subject, '', to=[user.email])
                email_message.attach_alternative(email_body, 'text/html')
                email_message.send()
        except Exception as e:
                return f"Failed to send OTP to {email}: {str(e)}"
        
        