from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import operator
from .models import *


class PairC:
    name = " "
    count = 0
    name2 = ""
    rank = 0

    def __init__(self, name, count):
        self.name = name
        self.count = count

    def setRank(self, r):
        self.rank = r

    def setName(self, name2):
        self.name2 = name2


# Create your views here.

def signup(request):
    if request.method == 'POST':
        ufname1 = request.POST.get('ufname1')
        ulname1 = request.POST.get('ulname1')
        ufname2 = request.POST.get('ufname2')
        ulname2 = request.POST.get('ulname2')
        uname = request.POST.get('uname')
        uemail = request.POST.get('uemail')
        upwd = request.POST.get('upwd')
        try:
            user = User.objects.create_user(username=uname, email=uemail, password=upwd, first_name=ufname1,
                                            last_name=ulname1)
            p = Player.objects.create(fname1=ufname1, lname1=ulname1, fname2=ufname2, lname2=ulname2, uid=user)
            u2 = authenticate(request, username=uname, password=upwd)
            p.save()
            login(request, u2)
            return render(request, 'questionpage.html')
                #return HttpResponseRedirect("/team")
        except Exception :
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
        # return HttpResponseRedirect("/team")
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
            #return render(request, 'questionpage.html')
            return HttpResponseRedirect("/team")
    out = "Username Password Combination does not match."
    context = {
        'out': out
    }
    return render(request, "index.html", context)


def questionadd(request):
    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST["title"]
        code = request.POST["code"]
        ans = request.POST["ans"]
        ques = Questions.objects.create(title=title, code=code, ans=ans)
        queadd = Queadd.objects.create(qid=ques, uid=request.user)
        queadd.save()
        return render(request, "questionpage.html")
    return HttpResponseRedirect("/")


def qutionchange(request, idv):
    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST["title"]
        code = request.POST["code"]
        ans = request.POST["ans"]
        q = Queadd.objects.get(id=idv)
        if q.uid == request.user:
            que = q.qid
            que.title = title
            que.code = code
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
                'q': que
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
        p = Player.objects.get(uid=i)
        name = i.first_name + " " + i.last_name
        pair = PairC(name, qc)
        pair.setName(p.fname2 + " " + p.lname2)
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
        check = Stream.objects.filter(uid=request.user)
        if not check:
            v = 2
        else:
            v = check[0].choice
        fe = Stream.objects.filter(choice=1).count()
        be = Stream.objects.filter(choice=2).count()
        context = {
            'fe': fe,
            'be': be,
            'v': v
        }
        return render(request, "vote.html", context)
    return HttpResponseRedirect("/")


def voteSubmit(request):
    if request.user.is_authenticated:
        s = request.POST['team']
        check = Stream.objects.filter(uid=request.user).first()
        if not check:
            pc = Stream.objects.create(uid=request.user, choice=s)
        else:
            check.choice = s
            check.save()
        return team(request)
    return HttpResponseRedirect("/")


def team(request):
    fe = Stream.objects.filter(choice=1)
    be = Stream.objects.filter(choice=2)
    vector1 = []
    count = 1
    for i in fe:
        name = i.uid.first_name + " " + i.uid.last_name
        pair = PairC(name, count)
        if i.uid.is_staff == 0:
            count += 1
            vector1.append(pair)
    vector2 = []
    count = 1
    for i in be:
        name = i.uid.first_name + " " + i.uid.last_name
        pair = PairC(name, count)
        if i.uid.is_staff == 0:
            count += 1
            vector2.append(pair)
    context = {
        'fe': vector1,
        'be': vector2
    }
    return render(request, "team.html", context)
