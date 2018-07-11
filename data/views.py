from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import operator
from .models import *


class PairC:
    name = " "
    count = 0
    rank = 0

    def __init__(self, name, count):
        self.name = name
        self.count = count

    def setRank(self, r):
        self.rank = r


# Create your views here.

def signup(request):
    if request.method == 'POST':
        ufname = request.POST.get('ufname')
        ulname = request.POST.get('ulname')
        uname = request.POST.get('uname')
        uemail = request.POST.get('uemail')
        upwd = request.POST.get('upwd')
        try:
            user = User.objects.create_user(username=uname, email=uemail, password=upwd, first_name=ufname,
                                            last_name=ulname)
            u2 = authenticate(request, username=uname, password=upwd)
            login(request, u2)
            return render(request, 'questionpage.html')
        except Exception:
            out = "Enter Different Username"
            context = {
                'out': out
            }
            return render(request, 'index.html', context)
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
    out = "Username Password Combination does not match."
    context = {
        'out': out
    }
    return render(request, "index.html", context)


def questionadd(request):
    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST["title"]
        oa = request.POST["oa"]
        ob = request.POST["ob"]
        oc = request.POST["oc"]
        od = request.POST["od"]
        ans = request.POST["answer"]
        ques = Questions.objects.create(title=title, oa=oa, ob=ob, oc=oc, od=od, ans=ans)
        print(ans)
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
        vector = []
        m = 1
        for i in q:
            pair = PairC(i.qid.title, m)
            pair.setRank(i.id)
            m += 1
            vector.append(pair)
        context = {
            'q': vector,
        }
        return render(request, "uploads.html", context)
    return HttpResponseRedirect("/")


def change(request, iv):
    if request.user.is_authenticated:
        try:
            q = Queadd.objects.get(id=iv)
        except Exception:
            return HttpResponseRedirect("/")
        if q.uid == request.user:
            que = q.qid
            print(que.ans)
            context = {
                'que': que
            }
        return render(request, "questionupdate.html", context)
    return HttpResponseRedirect("/")


def logoutfunc(request):
    logout(request)
    return render(request, "index.html")


def leardboard(request):
    q = User.objects.filter(is_staff=0)
    vector = []
    for i in q:
        qc = Queadd.objects.filter(uid=i).count()
        name = i.first_name + " " + i.last_name
        pair = PairC(name, qc)
        vector.append(pair)
    vector.sort(key=operator.attrgetter('count'))
    vector.reverse()
    rk = 1
    for i in vector:
        i.setRank(rk)
        rk += 1
    context = {
        'v': vector
    }
    return render(request, "leaderboard.html", context)


def votePage(request):
    if request.user.is_authenticated:
        check = stream.objects.get(uid=request.user)
        if check is None:
            v = 2
        else:
            v = check.choice
        fe = stream.objects.filter(choice=1).count()
        be = stream.objects.filter(choice=2).count()
        context = {
            'fe': fe,
            'be': be,
            'ch': v
        }
        return render(request, "vote.html", context)
    return HttpResponseRedirect("/")


def votePage(request):
    if request.user.is_authenticated:
        s = request.POST['team']
        check = stream.objects.get(uid=request.user)
        if check is None:
            pc = User.objects.create_user(uid=request.user, choice=s)
        else:
            check.choice = s
            check.save()
        return render(request, "vote.html", context)
    return HttpResponseRedirect("/")
