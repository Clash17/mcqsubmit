from django.shortcuts import render
from django.http import  Httpresponse
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

        user = User.objects.create_user(username = uname, email = uemail, password = upwd , first_name = ufname, last_name = ulname )

        u2 = authenticate(request, username = uname , password = upwd)

        login(request, u2)

        return render(request, 'question.html')
    else:
        return render(request, 'index.html')


def loginPage(request):
    return render(request, "index.html")



def questionadd(request):
    tilte = request.POST["title"]
    oa = request.POST["oa"]
    ob = request.POST["ob"]
    oc = request.POST["oc"]
    od = request.POST["od"]
    ans = request.POST["ans"]
