from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('/inventory/book/')
    context={
        "error":""
    }
    
    if request.method=='POST':
        user=authenticate(username=request.POST['username'],password=request.POST['password'])
        print(user)
        if user is not None:
            login(request,user)
            return redirect('/inventory/book/')
        else:
            context={
                "error":"inavalid username"
            }
        return render(request,'login.html',context)
    return render(request,'login.html',context)
def logoutpage(request):
    logout(request)
    return redirect("/")
def signup(request):
    context={
        "error":""
    }
    if request.method=='POST':
        user_check=user.objects.filter(username=request.POST['username'])
        if len(user_check)>0:
            context={
                "error":"username already exist"
            }
            return render(request,'signup.html',context)
        else:
        
            new_user=user(username=request.POST['username'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],
                email=request.POST['email'])
            new_user.set_password(request.POST['password'])
            new_user.save()
            return redirect('/')
    return render(request,'signup.html',context)
        

