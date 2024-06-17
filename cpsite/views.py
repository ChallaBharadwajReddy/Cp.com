from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from lockout_page.models import ForcesId
from .forms import LoginForm
import requests

def HomePage(request):
    try:
        forces=ForcesId.objects.get(player=request.user)
        handel=forces.handel
        print(handel)
    except:
        handel="--1"
    
    if request.method=="POST":
        new_handel=request.POST.get("new_handel")
        url="https://codeforces.com/api/user.status?handle="+new_handel
        response = requests.get(url)
        data = response.json()

        if data["status"] == "OK":
            print("OK")
            forcesid=ForcesId(player=request.user , handel = new_handel)
            forcesid.save()
            return redirect("home")
        else:
            return redirect("home")
    context={"handel":handel}
    return render(request,"main.html",context)

def LoginPage(request):
    page="login"
    if request.user.is_authenticated:
        return redirect('lockout')
    
    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
            print("user:",user)
        except:
            redirect('login')

        user=authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('home')
        else :
            return redirect("login")
    context={"page":page}
    return render(request,"loginPage.html",context)

def logOut(request):
    logout(request)
    return redirect('home')

def RegisterPage(request):
    page="register"

    if request.method == "POST":
        user=User(username=request.POST.get("username") , password=request.POST.get("password"))
        user.save()
        login(request,user)
        return redirect("home")
    context={"page":page}
    return render(request,"loginPage.html",context)