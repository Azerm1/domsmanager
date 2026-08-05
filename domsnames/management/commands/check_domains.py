from django.core.management.base import BaseCommand
from domsnames.models import domsname
from domsnames.services import remaining
from domsnames.email import send_notification
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        domains = domsname.objects.all()
        for domain in domains:
            days = remaining(domain.enddate)
            if days == 30 and not domain.notification_30:
                print("Sending J-30 email...")
                send_notification(domain,30)
                domain.notification_30 = True
                domain.save()
            elif days == 15 and not domain.notification_15:
                send_notification(domain,15)
                domain.notification_15 = True
                domain.save()
            elif days<=7 and not domain.notification_7:
                send_notification(domain,7)
                domain.notification_7 = True
                domain.save()
            elif days == 1 and not domain.notification_1:
                send_notification(domain,1)
                domain.notification_1 = True
                domain.save()
            elif days < 0 and not domain.notification_expired:
                send_notification(domain,0)
                domain.notification_expired = True
                domain.save()