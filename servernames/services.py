from datetime import date
def remaining(enddate):
    if isinstance(enddate, str):
        enddate=date.fromisoformat(enddate)
    return (enddate-date.today()).days
print (remaining('2027-01-01'))
def statut(enddate):
    days=remaining(enddate)
    if days>30:
        return 'active'
    elif 0<days<=30:
        return 'warning'
    else:return 'expired'
def message(enddate):
    days=remaining(enddate)
    if statut(enddate)=='active':return 'il reste',days,' jours'
    elif statut(enddate)=='warning':return 'Attention, expire dans',days,'jours'
    else: return 'expirer depuis',days,'jours'
def showlist(l):
    leatestaddedserver=[]
    n=len(l)
    i=0
    while i<5:
        try:
            leatestaddedserver.append(l[n-i])
        except:
            return leatestaddedserver