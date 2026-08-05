from django.shortcuts import render,redirect,get_object_or_404
from .models import servername
from .serverform import serverform
from .services import *
from dashboard.views import dashboard_context
from django.contrib.auth.decorators import login_required

@login_required()
def serverlist(request):
    servernames = servername.objects.all()
    search = request.GET.get("search")
    if search:
        servernames = servernames.filter(name__icontains=search)
    for server in servernames:
        server.days=remaining(server.enddate)
        server.statut=statut(server.enddate)
        server.message=message(server.enddate)
    return render(request, 'listserver.html', {'servernames': servernames[::-1]})

def serveradd(request):
    servernames = servername.objects.all()
    l=[]
    for server in servernames:
        l.append({"object": server, "startdate": server.startdate, "statut": statut(server.enddate)})
    l.sort(key=lambda x: x['startdate'] or date.max)
    leatestaddedservers=showlist(l)
    n=len(l)
    if request.method == 'POST':
        form = serverform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('serverlist')
    else:form = serverform()
    return render(request, 'addserver.html', {'form': form,'leatestaddedservers':leatestaddedservers,'n':n})

def serveredit(request,id):
    servernames = servername.objects.all()
    server= get_object_or_404(servername, id=id)
    if request.method=='POST':
        form = serverform(request.POST, instance=server)
        if form.is_valid():
            server = form.save(commit=False)

            server.notification_30 = False
            server.notification_15 = False
            server.notification_7 = False
            server.notification_1 = False
            server.notification_expired = False

            server.save()
            return redirect('serverlist')
    else:form=serverform(instance=server)
    return render(request, 'serveredit.html', {'form': form,'object': server})

def serverdel(request,id):
    servernames = servername.objects.all()
    server= get_object_or_404(servername, id=id)
    if request.method=='POST':
        server.delete()
        return redirect('serverlist')
    return render(request,'delete.html',{'object': server})

def activeserver(request):
    servernames = servername.objects.all()
    actives = []
    for server in servernames:
        server.days = remaining(server.enddate)
        server.statut = statut(server.enddate)
        if server.statut == "active":
            actives.append(server)
    return render(request, "listserver.html", {"servernames": actives})
def warningserver(request):
    servernames = servername.objects.all()
    warnings=[]
    for server in servernames:
        server.statut=statut(server.enddate)
        if server.statut=='warning':
            warnings.append(server)
    return render(request, 'listserver.html', {'servernames': warnings})

def expiredserver(request):
    servernames = servername.objects.all()
    expired=[]
    for server in servernames:
        server.statut=statut(server.enddate)
        if server.statut=='expired':
            expired.append(server)
    return render(request, 'listserver.html', {'servernames': expired})