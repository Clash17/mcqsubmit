from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import *


# Create your views here.

def signup(request):
    if request.method == 'POST':
        ufname = request.POST.get('ufname')
        ulname = request.POST.get('ulname')
        uname = request.POST.get('uname')
        uemail = request.POST.get('uemail')
        upwd = request.POST.get('upwd')
        user = User.objects.create_user(username=uname, email=uemail, password=upwd, first_name=ufname,
                                        last_name=ulname)
        u2 = authenticate(request, username=uname, password=upwd)
        login(request, u2)
        return render(request, 'questionpage.html')
    else:
        return render(request, 'index.html')


def loginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/questionpage")
    return render(request, "index.html")


def addque(request):
    if request.user.is_authenticated:
        return render(request, "questionpage.html")
    return render(request, "index.html")


def loginfunc(request):
    if request.method == 'POST':
        uname = request.POST["uname"]
        upwd = request.POST["upwd"]
        u2 = authenticate(request, username=uname, password=upwd)
        if u2 is not None:
            login(request, u2)
            return render(request, 'questionpage.html')
    return render(request, "index.html")


def questionadd(request):
    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST["title"]
        oa = request.POST["oa"]
        ob = request.POST["ob"]
        oc = request.POST["oc"]
        od = request.POST["od"]
        ans = request.POST["answer"]
        ques = Questions.objects.create(title=title, oa=oa, ob=ob, oc=oc, od=od, ans=ans)
        queadd = Queadd.objects.create(qid=ques, uid=request.user)
        return render(request, "questionpage.html")
    return HttpResponseRedirect("/")


def qutionchange(request, idv):
    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST["title"]
        oa = request.POST["oa"]
        ob = request.POST["ob"]
        oc = request.POST["oc"]
        od = request.POST["od"]
        ans = request.POST["answer"]
        q = Queadd.objects.get(id=idv)
        if q.uid == request.user:
            que = q.qid
            que.title = title
            que.oa = oa
            que.ob = ob
            que.oc = oc
            que.od = od
            que.ans = ans
            que.save()
            return HttpResponseRedirect("/uploads")
    return HttpResponseRedirect("/")


def uploads(request):
    if request.user.is_authenticated:
        q = Queadd.objects.filter(uid=request.user)
        m = 0
        context = {
            'q' : q,
            'm' : m
        }
        return render(request, "uploads.html", context)
    return HttpResponseRedirect("/")


def change(request, iv):
    if request.user.is_authenticated :
        try:
            q = Queadd.objects.get(id=iv)
        except Exception:
            return HttpResponseRedirect("/")
        if q.uid == request.user:
            que = q.qid
            context = {
                'que': que
            }
        return render(request, "questionupdate.html", context)
    return HttpResponseRedirect("/")


def logoutfunc(request):
    logout(request)
    return render(request, "index.html")
