from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


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
    tilte = request.POST["title"]
    oa = request.POST["oa"]
    ob = request.POST["ob"]
    oc = request.POST["oc"]
    od = request.POST["od"]
    ans = request.POST["ans"]
    return HttpResponse("hello")


def logoutfunc(request):
    logout(request)
    return render(request, "index.html")
