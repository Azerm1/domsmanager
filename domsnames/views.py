from django.shortcuts import render,redirect,get_object_or_404
from .models import domsname
from .domsform import domsform
from .services import *
from dashboard.views import dashboard_context
# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required()
def domslist(request):
    domsnames = domsname.objects.all()
    search = request.GET.get("search")
    if search:
        domsnames = domsnames.filter(name__icontains=search)
    for domain in domsnames:
        domain.days=remaining(domain.enddate)
        domain.statut=statut(domain.enddate)
        domain.message=message(domain.enddate)
    return render(request, 'listdoms.html', {'domsnames': domsnames[::-1]})

def domsadd(request):
    domsnames = domsname.objects.all()
    l=[]
    for domain in domsnames:
        l.append({"object": domain, "startdate": domain.startdate, "statut": statut(domain.enddate)})
    l.sort(key=lambda x: x['startdate'] or date.max)
    leatestaddeddoms=showlist(l)
    n=len(l)
    if request.method == 'POST':
        form = domsform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('domslist')
    else:form = domsform()
    return render(request, 'adddoms.html', {'form': form,'leatestaddeddoms':leatestaddeddoms,'n':n})

def domsedit(request,id):
    domsnames = domsname.objects.all()
    domain= get_object_or_404(domsname, id=id)
    if request.method=='POST':
        form = domsform(request.POST, instance=domain)
        if form.is_valid():
            domain = form.save(commit=False)

            domain.notification_30 = False
            domain.notification_15 = False
            domain.notification_7 = False
            domain.notification_1 = False
            domain.notification_expired = False

            domain.save()
            return redirect('domslist')
    else:form=domsform(instance=domain)
    return render(request, 'editdoms.html', {'form': form,'object': domain})

def domsdel(request,id):
    domsnames = domsname.objects.all()
    domain= get_object_or_404(domsname, id=id)
    if request.method=='POST':
        domain.delete()
        return redirect('domslist')
    return render(request,'delete.html',{'object': domain})

def activedoms(request):
    domsnames = domsname.objects.all()
    actives = []
    for domain in domsnames:
        domain.days = remaining(domain.enddate)
        domain.statut = statut(domain.enddate)
        if domain.statut == "active":
            actives.append(domain)
    return render(request, "listdoms.html", {"domsnames": actives})
def warningdoms(request):
    domsnames = domsname.objects.all()
    warnings=[]
    for domain in domsnames:
        domain.statut=statut(domain.enddate)
        if domain.statut=='warning':
            warnings.append(domain)
    return render(request, 'listdoms.html', {'domsnames': warnings})

def expireddoms(request):
    domsnames = domsname.objects.all()
    expired=[]
    for domain in domsnames:
        domain.statut=statut(domain.enddate)
        if domain.statut=='expired':
            expired.append(domain)
    return render(request, 'listdoms.html', {'domsnames': expired})