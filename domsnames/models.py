from django.db import models

# Create your models here.
class domsname(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=50,default='')
    startdate=models.DateField(null=True, blank=True,default='NULL')
    enddate=models.DateField()
    email = models.EmailField(blank=True,default="amine@digest-media.agency")
    notification_30 = models.BooleanField(default=False)
    notification_15 = models.BooleanField(default=False)
    notification_7 = models.BooleanField(default=False)
    notification_1 = models.BooleanField(default=False)
    notification_expired = models.BooleanField(default=False)

class Notification(models.Model):
    domain = models.ForeignKey(
        'domsname',
        on_delete=models.CASCADE,
        related_name='notifications')
    recipient = models.EmailField()
    days_before = models.IntegerField()
    sent_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.domain.name} - {self.recipient}"