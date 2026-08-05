from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from email.mime.image import MIMEImage
from .models import Notification
import os

User = get_user_model()


def send_notification(domain, days):

    admin = User.objects.get(id=2)

    subject = f"Domain Notification - {domain.name}"

    html = render_to_string(
        "domains_notifs.html",
        {
            "domain": domain,
            "days": days,
        },
    )

    email = EmailMultiAlternatives(
        subject,
        f"The domain {domain.name} expires in {days} day(s).",
        settings.DEFAULT_FROM_EMAIL,
        [admin.email],
    )

    email.attach_alternative(html, "text/html")

    logo_path = os.path.join(
        settings.BASE_DIR,
        "dashboard",
        "static",
        "logo.png",
    )

    with open(logo_path, "rb") as f:
        logo = MIMEImage(f.read())

    logo.add_header("Content-ID", "<logo>")
    logo.add_header(
        "Content-Disposition",
        "inline",
        filename="logo.png",
    )

    email.attach(logo)

    email.send()

    Notification.objects.create(
        domain=domain,
        recipient=admin.email,
        days_before=days,
    )