from django.shortcuts import render
from domsnames.models import domsname
from servernames.models import servername
from users.models import User
from domsnames.services import *
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def dashboard(request):
    domains = domsname.objects.all()
    servers = servername.objects.all()
    users=User.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
        role= request.user.role
    else:
        username = "Guest"
        role= "guest"

    active_domains = 0
    warning_domains = 0
    expired_domains = 0
    active_servers = 0
    warning_servers = 0
    expired_servers = 0
    expired_list=[]
    leatest_expired=[]
    for domain in domains:
        domain_status = statut(domain.enddate)
        days=remaining(domain.enddate)
        if domain_status == "active":active_domains += 1
        elif domain_status == "warning":warning_domains += 1
        else:
            expired_list.append({
                "type": "Domain",
                "object": domain,
                "days": days})
            expired_domains += 1
    for server in servers:
        server_status = statut(server.enddate)
        days=remaining(server.enddate)
        if server_status == "active":active_servers += 1
        elif server_status == "warning":warning_servers += 1
        else:
            expired_list.append({
                "type": "Server",
                "object": server,
                "days": days})
            expired_servers += 1
    expired_list.sort(key=lambda x: x["days"])
    leatest_expired=expired_list[:len(expired_list)%4]

    l= []
    for domain in domains:
        days = remaining(domain.enddate)
        if 0 <= days <= 5:
            l.append({
                "type": "Domain",
                "object": domain,
                "days": days})
    for server in servers:
        days = remaining(server.enddate)
        if 0 <= days <= 10:
            l.append({
                "type": "Server",
                "object": server,
                "days": days})
    l.sort(key=lambda x: x["days"])
    close_to_expire = l[:4]
    close_to_expire_nbre =len(l)

    context = {
        "total_domains": domains.count(),
        "total_servers": servers.count(),
        "total_users": users.count(),
        "total_users": User.objects.count(),
        "active_domains": active_domains,
        "warning_domains": warning_domains,
        "expired_domains": expired_domains,
        "active_servers": active_servers,
        "warning_servers": warning_servers,
        "expired_servers": expired_servers,
        'role':role,
        'username':username,
        "expired_list":expired_list,
        "close_to_expire":close_to_expire,
        "close_to_expire_nbre":close_to_expire_nbre,
        "leatest_expired":leatest_expired,
        'expired_list':expired_list}
    return render(request, "dashboard.html", context)

def dashboard_context(request):
    domains = domsname.objects.all()
    servers = servername.objects.all()
    users=User.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
        role= request.user.role
    else:
        username = "Guest"
        role= "smthng"

    active_domains = 0
    warning_domains = 0
    expired_domains = 0
    active_servers = 0
    warning_servers = 0
    expired_servers = 0
    expired_list=[]
    leatest_expired=[]
    for domain in domains:
        domain_status = statut(domain.enddate)
        days=remaining(domain.enddate)
        if domain_status == "active":active_domains += 1
        elif domain_status == "warning":warning_domains += 1
        else:
            expired_list.append({
                "type": "Domain",
                "object": domain,
                "days": days})
            expired_domains += 1
    for server in servers:
        server_status = statut(server.enddate)
        days=remaining(server.enddate)
        if server_status == "active":active_servers += 1
        elif server_status == "warning":warning_servers += 1
        else:
            expired_list.append({
                "type": "Server",
                "object": server,
                "days": days})
            expired_servers += 1
    expired_list.sort(key=lambda x: x["days"])
    leatest_expired=expired_list[:len(expired_list)%4]

    l= []
    for domain in domains:
        days = remaining(domain.enddate)
        if 0 <= days <= 5:
            l.append({
                "type": "Domain",
                "object": domain,
                "days": days})
    for server in servers:
        days = remaining(server.enddate)
        if 0 <= days <= 10:
            l.append({
                "type": "Server",
                "object": server,
                "days": days})
    l.sort(key=lambda x: x["days"])
    close_to_expire = l[:4]
    close_to_expire_nbre =len(l)

    context = {
        "total_domains": domains.count(),
        "total_servers": servers.count(),
        "total_users": users.count(),
        "total_users": User.objects.count(),
        "active_domains": active_domains,
        "warning_domains": warning_domains,
        "expired_domains": expired_domains,
        "active_servers": active_servers,
        "warning_servers": warning_servers,
        "expired_servers": expired_servers,
        'role':role,
        'username':username,
        "expired_list":expired_list,
        "close_to_expire":close_to_expire,
        "close_to_expire_nbre":close_to_expire_nbre,
        "leatest_expired":leatest_expired,
        'expired_list':expired_list}
    return context

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from domsnames.services import check_domain
from servernames.services import check_server


@csrf_exempt
def cron_check_expirations(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    check_domain()
    check_server()

    return JsonResponse({
        "status": "success",
        "message": "Domains and servers checked"
    })