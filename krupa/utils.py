from django.conf import settings
from django.core.mail import send_mail


def send_email_token(email,id):
    # print(email)
    # print(email_token)
    try:
        subject = 'Estimates are sent'
        message = f'Click on the link to verify http://127.0.0.1:8000/billing/{id}/'
        email_form = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail(subject,message,email_form,recipient_list)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
    
    return True