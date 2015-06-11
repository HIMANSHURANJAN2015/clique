import datetime
from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from app.models import Account,Accountinfo
from clique.settings import MEDIA_ROOT
import os

def home(request):
	return render_to_response('homepage.html',context_instance=RequestContext(request))

def signup(request):
    #print("called")
    return render_to_response('signup.html',context_instance=RequestContext(request))

def login(request):
    #print("called")
    return render_to_response('loginpage.html',context_instance=RequestContext(request))

def loginverify(request):
    if request.method=="POST":
        inputemail=request.POST.get('inputEmail')
        inputpass=request.POST.get('inputPassword')
        try:
            account1=Account.objects.get(email=inputemail)
            name=account1.name
            pwd=account1.password
            request.session['name'] = name
            request.session['email'] = inputemail
            
            #img=str(Accountinfo.objects.get(email=inputemail).pic)
            #print(img)
            
            #print(Accountinfo.objects.get(email=inputemail).pic)
            if pwd==inputpass:
                #img=os.path.join(MEDIA_ROOT,Accountinfo.objects.get(email=inputemail).pic)
                #print(img)
                #img=str(Accountinfo.objects.get(email=inputemail).pic)
                try:
                    a=Accountinfo.objects.get(email=inputemail)
                    img=str(a.pic)
                    print(img)
                    return render(request,'profile.html',{"name":name,'imageurl':img})
                except:
                    return render(request,'profile.html',{"name":name,'imageurl':None})
            else:
                return render(request,'error.html',{"error":"incorrect password"})
        except Exception as e:
            print(e)
            return render(request,'error.html',{"error":"There is no account with the given email id !! "})
def signupverify(request):
    if request.method=="POST":
        inputname=request.POST.get('name')
        inputemail=request.POST.get('email')
        inputpass=request.POST.get('password')
        inputdobd=request.POST.get('bd')
        inputdobm=request.POST.get('bm')
        inputdoby=request.POST.get('by')
     
        try:
            account1=Account.objects.get(email=inputemail)
            return render(request,'error.html',{"error":"EMAIL IS ALREADY REGISTERED !!!"})
        except:
            account1=Account(email=inputemail,password=inputpass,name=inputname,dob_d=inputdobd,dob_m=inputdobm,dob_y=inputdoby)
            account1.save()
            return render(request,'success.html',{"message":"congrats","name":inputname})
        '''
        account1=Account(email=inputemail,password=inputpass,name=inputname,dob_d=inputdobd,dob_m=inputdobm,dob_y=inputdoby)
        account1.save()
        return render(request,'success.html',{"message":"congrats","name":inputname})
        '''

def uploadpic(request):
    if request.method=="POST":
        imail=request.POST.get('inputemail')
        dbaccount=Account.objects.get(email=imail)
        ifile=request.POST.get('inputfile')
        print(type(ifile))
        iabout=request.POST.get('inputabout')
        account1=Accountinfo(email=dbaccount,pic=ifile,about=iabout)
        account1.save()
        print(ifile)
        return render(request,'success.html',{"message":"congrats","name":imail})





