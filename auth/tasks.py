from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# RESET PASSWORD EMAIL
@shared_task
def send_password_reset_email_task(email, reset_url):
    subject = "Reset Your Password"

    html_content = render_to_string(
        "auth/emails/reset_password.html",
        {"reset_url": reset_url},
    )

    text_content = (
        "Hello,\n\n"
        "We received a request to reset the password "
        "for your account.\n\n"
        "Use the link below to set a new password:\n"
        f"{reset_url}\n\n"
        "This link expires according to your password-reset policy.\n\n"
        "If you did not request a password reset, you can ignore "
        "this email. Your password will remain unchanged unless "
        "the reset process is completed.\n\n"
        "Best regards,\n"
        "The Security Team"
    )

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )

    email_message.attach_alternative(
        html_content,
        "text/html",
    )

    email_message.send(fail_silently=False)

#OTP Request
@shared_task
def send_login_otp_email_task(email, otp):
    subject = "Login OTP"

    html_content = render_to_string(
        "auth/emails/login_otp.html",
        {"otp": otp},
    )

    text_content = (
        "Hello,\n\n"
        "We received a request to sign in to your account.\n\n"
        f"Your login verification code is: {otp}\n\n"
        "This code expires in 3 minutes.\n\n"
        "Never share this code with anyone.\n\n"
        "If you did not attempt to log in, "
        "please ignore this email and secure your account "
        "if you suspect unauthorized access.\n\n"
        "Best regards,\n"
        "The Security Team"
    )

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )

    email_message.attach_alternative(
        html_content,
        "text/html",
    )

    email_message.send(fail_silently=False)