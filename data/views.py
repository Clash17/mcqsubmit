from django.shortcuts import render


# Create your views here.
def loginPage(request):
    return render(request, "index.html")



def questionadd(request):
    tilte = request.POST["title"]
    oa = request.POST["oa"]
    ob = request.POST["ob"]
    oc = request.POST["oc"]
    od = request.POST["od"]
    ans = request.POST["ans"]
