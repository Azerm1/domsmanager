from django.contrib import admin
from .models import domsname
from .models import Notification
# Register your models here.
admin.site.register(domsname)
admin.site.register(Notification)