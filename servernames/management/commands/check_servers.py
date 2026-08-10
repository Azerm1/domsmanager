from django.core.management.base import BaseCommand
from servernames.models import servername
from servernames.services import remaining
from servernames.email import send_notification


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        servers = servername.objects.all()

        for server in servers:
            days = remaining(server.enddate)

            if days == 30 and not server.notification_30:
                send_notification(server, 30)
                server.notification_30 = True
                server.save()

            elif days == 15 and not server.notification_15:
                send_notification(server, 15)
                server.notification_15 = True
                server.save()

            elif 1 < days <= 7 and not server.notification_7:
                send_notification(server, 7)
                server.notification_7 = True
                server.save()

            elif days == 1 and not server.notification_1:
                send_notification(server, 1)
                server.notification_1 = True
                server.save()

            elif days < 0 and not server.notification_expired:
                send_notification(server, 0)
                server.notification_expired = True
                server.save()