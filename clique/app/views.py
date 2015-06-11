import datetime
from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from app.models import Account,Accountinfo,Friends
from clique.settings import MEDIA_ROOT
from collections import OrderedDict
import os
from azure.storage import TableService, Entity

def friend_email_get(mine):
    l=[]
    try:
        # will return a list of email ids of freinds
        table_service = TableService(account_name='clique', account_key='zMSzhIxowjBuMvLo24CUcIA1r5EaMaLgYPvblm6JxS4EkHZEFbMXuwv2XWirMppLA9Hb8m3mx92Zg0pNxICzYw==')
        #since table is already created
        #table_service.create_table('friendstable')
        tuple1 = table_service.get_entity('friendlisttable', 'friend', mine)
        count=tuple1.count
        for i in range(1,count+1):
            field="friend"+str(i);
            k_dict=tuple1.__dict__
            print("\n\n",k_dict,"\n\n") 
            data=k_dict[field]
            print("\n\n",data)
            l.append(data)
        print("\n\n",l,"\n\n")
    except Exception as e:
        print(e)
    return l

def friend_email_add(mine,friend):
    #SEE if my tuple is there .. is not then create and add else simple merge
    print("\n\n\n\n\ running addin table ")
    table_service = TableService(account_name='clique', account_key='zMSzhIxowjBuMvLo24CUcIA1r5EaMaLgYPvblm6JxS4EkHZEFbMXuwv2XWirMppLA9Hb8m3mx92Zg0pNxICzYw==')
    try:
        task = table_service.get_entity('friendlisttable', 'friend', mine)
        count=task.count
        print(count)
        field="friend"+str(count+1)
        data={field:friend,'count':(count+1)}
        table_service.insert_or_merge_entity('friendlisttable','friend',mine,data)
        print("value 1 inserted via merge")
    except Exception as e:
        print(e)
        print("your account was not there")
        data= {'PartitionKey':'friend','RowKey':mine,'count':1,'friend1':friend}
        table_service.insert_entity('friendlisttable', data)
        print("value 1 added via create")
    try:
        task = table_service.get_entity('friendlisttable', 'friend', friend)
        count=task.count
        print(count)
        field="friend"+str(count+1)
        data={field:mine,'count':(count+1)}
        table_service.insert_or_merge_entity('friendlisttable','friend',friend,data)
        print("value 2 inserted via merge")
    except Exception as e:
        print(e)
        print("your account was not there")
        data= {'PartitionKey':'friend','RowKey':friend,'count':1,'friend1':mine}
        table_service.insert_entity('friendlisttable', data)
        print("value 2 added via create")
    print("added al \n\n\n ")


    

def home(request):
    #print("Starting",request.session['email'])
	return render_to_response('homepage.html',context_instance=RequestContext(request))

def signup(request):
    #print("called")
    return render_to_response('signup.html',context_instance=RequestContext(request))

def login(request):
    #print("called")
    return render_to_response('loginpage.html',context_instance=RequestContext(request))

def removeduplicate(l):
    #list(OrderedDict.fromkeys(l))          ### hashing will not work here since we have dictionary!!
    #return l
    '''
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    '''
    output=[dict(tupleized) for tupleized in set(tuple(item.items()) for item in l)]
    return output

def loginverify(request='asd'):
    if request=='asd':
        return render_to_response('loginpage.html',context_instance=RequestContext(request))

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
                    img=""
                    a=Accountinfo.objects.filter(email=inputemail)
                    if(len(a) == 0):
                        img="assets/uploaded_files/1429885540_94804_profile.jpg"
                    else:
                        img=str(a[0].pic)
                    print(img)
                    request.session['email']=inputemail
                    print("\n New session set ",request.session['email'],"\n")
                    ####now i will find friends
                    
                    #flist=Friends.objects.filter(this_account=Account.objects.filter(email=inputemail))
                    flistemail=[]
                    print("0")
                    #for i in flist:
                    #    print(i.friend_account)
                    #    flistemail.append(i.friend_account)
                    print("1")
                    flistemail=friend_email_get(inputemail)
                    flistname=[]
                    flistpic=[]
                    print("\n\n checking 2 \n\n",flistemail)
                    
                    for i in flistemail:
                        print(i)
                        x=Account.objects.filter(email=i)
                        print(x[0])
                        flistname.append(x[0].name)
                        y=Accountinfo.objects.filter(email=x[0])
                        print("\nThis value is causing problem",y,"\n")
                        if len(y) ==0:
                            print("in if")     ######## 
                            #print(y[0])
                            flistpic.append("assets/uploaded_files/1429885540_94804_profile.jpg")
                        else:
                            print("in else")
                            flistpic.append(y[0].pic)
                    print("\n",len(flistname),len(flistemail),len(flistpic))
                    print("2")
                    frienddictlist=[]
                    for i in range(len(flistname)):
                        d={'name':flistname[i],'email':flistemail[i],'pic':flistpic[i]}
                        frienddictlist.append(d)
                    print("\n\n changes made")
                    frienddictlist=removeduplicate(frienddictlist)
                    ##### so i removed the duplicate elements
                    req=FriendRequests.objects.filter(to_account=inputemail)
                    print(req)
                    reqfromemail=[]
                    for i in req:
                        x=i.from_account.email
                        reqfromemail.append(x)
                    print("\n\n\n i am about to send ")
                    c=len(reqfromemail)
                    print(c)  
                    activitylist=[]
                    for i in flistemail:
                        o=Activity2.objects.filter(by=Account.objects.filter(email=i))
                        for j in o:
                            activitylist.append(j)
                    activitylist.sort(key=lambda x:x.when,reverse=True)
                    activitydictlist=[]
                    for i in range(len(activitylist)):
                        d={"by":activitylist[i].by.email,"when":activitylist[i].when,"activity":activitylist[i].activity,"data":activitylist[i].data,"pic":activitylist[i].photo,"like":activitylist[i].like}
                        print("\n",d,"\n")
                        activitydictlist.append(d)
                    activitydictlist=removeduplicate(activitydictlist)
                    print("activitydictlist",activitydictlist)
                    '''
                    request.session['img']=img
                    request.session['flistemail']=flistemail
                    request.session['flistname']=flistname
                    request.session['flistpic']=flistpic
                    request.session['frienddictlist']=frienddictlist
                    request.session['reqfromemail']=reqfromemail
                    request.session['c']=c
                    request.session['activitylist']=activitylist'''
                    #a=Account.objects.get()
                    a=Account.objects.get(email=inputemail)
                    activity=[]
                    try:
                        activity=Activity2.objects.filter(by=a)
                        print(a)
                    except Exception as e:
                        activity=[]
                    activitydictlistmy=[]
                    for i in activity:
                        d={"when":i.when,"activity":i.activity,"data":i.data,"photo":i.photo,"like":i.like}
                        activitydictlistmy.append(d)
                    print(activitydictlistmy)


                    return render(request,'profile.html',{"name":name,'profilepic':img,"email":inputemail,"friendlistemail":flistemail,"friendlistname":flistname,"friendlistpic":flistpic,"frienddictionary":frienddictlist,"list_reqfromemail":reqfromemail,"count_request":c,"activitydictlist":activitydictlist,"uploadedphotos":activitydictlistmy})
                except Exception as e1:
                    print(e1)
                    return render(request,'profile.html',{"name":name,'profilepic':None,"email":inputemail})
            else:
                return render(request,'error.html',{"error":"incorrect username and password"})
        except Exception as e:
            print(e)
            return render(request,'error.html',{"error":"incorrect username and password "})
            #return render(request,'error.html',{"error":"There is no account with the given email id !! "})
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
            return render_to_response('loginpage.html',context_instance=RequestContext(request))
            #return render(request,'success.html',{"message":"congrats","name":inputname})
        '''
        account1=Account(email=inputemail,password=inputpass,name=inputname,dob_d=inputdobd,dob_m=inputdobm,dob_y=inputdoby)
        account1.save()
        return render(request,'success.html',{"message":"congrats","name":inputname})
        '''

def uploadpic(request):
    if request.method=="POST":
        imail=request.POST.get('inputemail')
        dbaccount=Account.objects.get(email=imail)
        #ifile=request.POST.get('inputfile')
        ifile=request.FILES['inputfile']
        print(type(ifile))
        iabout=request.POST.get('inputabout')
        account1=Accountinfo(email=dbaccount,pic=ifile,about=iabout)
        account1.save()
        print(ifile)
        return render(request,'success.html',{"message":"congrats","name":imail})
def refreshpage(request):
    
    inputemail=request.session['email']
    account1=Account.objects.get(email=inputemail)
    name=account1.name
    print("session received ",inputemail)
    try:
        #a=Accountinfo.objects.get(email=inputemail)
        img=""
        a=Accountinfo.objects.filter(email=inputemail)
        if(len(a) == 0):
            img="assets/uploaded_files/1429885540_94804_profile.jpg"
        else:
            img=str(a[0].pic)
        
        '''
        if a is not None:
            img=str(a.pic)
            print(img)
        '''
        #request.session['email']=inputemail
        #print("\n New session set ",request.session['email'],"\n")
        #flist=Friends.objects.filter(this_account=Account.objects.filter(email=inputemail))
        flistemail=[]                   #######stores email of all friend
        #for i in flist:
        #    flistemail.append(i.friend_account)
        flistemail=friend_email_get(inputemail)
        flistname=[]            
        flistpic=[]
        for i in flistemail:
            x=Account.objects.filter(email=i)
            flistname.append(x[0].name)
            y=Accountinfo.objects.filter(email=x[0])
            #if y is not None:
            #    flistpic.append(y[0].pic)
            if len(y) ==0:
                print("in if")     ######## 
                #print(y[0])
                flistpic.append("assets/uploaded_files/1429885540_94804_profile.jpg")
            else:
                print("in else")
                flistpic.append(y[0].pic)
        frienddictlist=[]
        for i in range(len(flistname)):
            d={'name':flistname[i],'email':flistemail[i],'pic':flistpic[i]}
            frienddictlist.append(d)
        frienddictlist=removeduplicate(frienddictlist)
        req=FriendRequests.objects.filter(to_account=inputemail)
        print(req)
        reqfromemail=[]
        for i in req:
            x=i.from_account.email
            reqfromemail.append(x)
        print("\n\n\n i am about to send ")
        c=len(reqfromemail) 
        print("\n\n",c,"\t",type(c))
        activitylist=[]
        for i in flistemail:
            o=Activity2.objects.filter(by=Account.objects.filter(email=i))
            for j in o:
                activitylist.append(j)
        activitylist.sort(key=lambda x:x.when,reverse=True)
        activitydictlist=[]
        for i in range(len(activitylist)):
            d={"by":activitylist[i].by.email,"when":activitylist[i].when,"activity":activitylist[i].activity,"data":activitylist[i].data,"pic":activitylist[i].photo,"like":activitylist[i].like}
            activitydictlist.append(d)
        print("activitydictlist",activitydictlist)
        #home(request)
        '''
        request.session['img']=img
        request.session['flistemail']=flistemail
        request.session['flistname']=flistname
        request.session['flistpic']=flistpic
        request.session['frienddictlist']=frienddictlist
        request.session['reqfromemail']=reqfromemail
        request.session['c']=c
        request.session['activitylist']=activitylist'''
        a=Account.objects.get(email=inputemail)
        activity=[]
        try:
            activity=Activity2.objects.filter(by=a)
            print(a)
        except Exception as e:
            activity=[]
        activitydictlistmy=[]
        for i in activity:
            d={"when":i.when,"activity":i.activity,"data":i.data,"photo":i.photo,"like":i.like}
            activitydictlistmy.append(d)
            print(activitydictlistmy)
        activitydictlistmy=removeduplicate(activitydictlistmy)
        return render(request,'profile.html',{"name":name,'profilepic':img,"email":inputemail,"friendlistemail":flistemail,"friendlistname":flistname,"friendlistpic":flistpic,"frienddictionary":frienddictlist,"list_reqfromemail":reqfromemail,"count_request":c,"activitydictlist":activitydictlist,"uploadedphotos":activitydictlistmy})
        #return render(request,'profile.html',{"name":name,'profilepic':img,"email":inputemail,"frienddictionary":frienddictlist,"list_reqfromemail":reqfromemail,"count_request":c,"activitydictlist":activitydictlist})
    except Exception as e:
        print(e)
        return render(request,'profile.html',{"name":name,"email":inputemail})

def acceptfriend(request):
    try:
        email = request.get_full_path()
        got = email.split('/')[-2]
        print("\n\n",request,"\n\n",got)
        ####### this account is my account
        
        this_email=request.session['email']
        this_account1=Account.objects.filter(email=this_email)[0]
        
        friend_account1=request.get_full_path().split('/')[-2]
        '''
        a=Friends(this_account=this_account1,friend_account=friend_account1)
        a.save()
        '''
        friend_email_add(this_email,friend_account1)
        print("added",friend_account1,"to ",this_account1)

        ###### this account is friwnds account
        
        this_account1=Account.objects.filter(email=got)[0]
        friend_account1=this_email
        '''
        a=Friends(this_account=this_account1,friend_account=friend_account1)
        a.save()
        '''
        print("added",friend_account1,"to",this_account1)
        
        ##### deleting friend requests #######
        r=FriendRequests.objects.filter(from_account=this_account1,to_account=friend_account1)
        r.delete()
        
        inputemail=request.session['email']
        #flist=Friends.objects.filter(this_account=Account.objects.filter(email=inputemail))
        flistemail=[]
        #for i in flist:
        #    flistemail.append(i.friend_account)
        flistemail=friend_email_get(inputemail)
        flistname=[]
        flistpic=[]
        for i in flistemail:
            x=Account.objects.filter(email=i)
            flistname.append(x[0].name)
            y=Accountinfo.objects.filter(email=x[0])
            if len(y) ==0:
                print("in if")     ######## 
                #print(y[0])
                flistpic.append("assets/uploaded_files/1429885540_94804_profile.jpg")
            else:
                print("in else")
                flistpic.append(y[0].pic)
        frienddictlist=[]
        for i in range(len(flistname)):
            d={'name':flistname[i],'email':flistemail[i],'pic':flistpic[i]}
            frienddictlist.append(d)
        
        print("\n\n changes made")
        frienddictlist=removeduplicate(frienddictlist)
        req=FriendRequests.objects.filter(to_account=inputemail)
        print(req)
        reqfromemail=[]
        for i in req:
            x=i.from_account.email
            reqfromemail.append(x)
            print("\n\n\n i am about to send ")
        c=len(reqfromemail)
        print(c)  
        activitylist=[]
        for i in flistemail:
            o=Activity2.objects.filter(by=Account.objects.filter(email=i))
            for j in o:
                activitylist.append(j)
                activitylist.sort(key=lambda x:x.when,reverse=True)
        activitydictlist=[]
        for i in range(len(activitylist)):
            d={"by":activitylist[i].by.email,"when":activitylist[i].when,"activity":activitylist[i].activity,"data":activitylist[i].data,"pic":activitylist[i].photo,"like":activitylist[i].like}
            print("\n",d,"\n")
            activitydictlist.append(d)
        print("activitydictlist",activitydictlist)
        activitydictlist=removeduplicate(activitydictlist)
        name=request.session['name']
        try:
            img=""
            a=Accountinfo.objects.filter(email=inputemail)
            if(len(a) == 0):
                img="assets/uploaded_files/1429885540_94804_profile.jpg"
            else:
                img=str(a[0].pic)
        except Exception as e:
            print(e)
            img=None
        '''
        img=request.session['img']
        request.session['flistemail']=flistemail
        request.session['flistname']=flistname
        request.session['flistpic']=flistpic
        request.session['frienddictlist']=frienddictlist
        request.session['reqfromemail']=reqfromemail
        request.session['c']=c
        request.session['activitylist']=activitylist'''
        a=Account.objects.get(email=inputemail)
        activity=[]
        try:
            activity=Activity2.objects.filter(by=a)
            print(a)
        except Exception as e:
            print(e)
            activity=[]
        activitydictlistmy=[]
        for i in activity:
            d={"when":i.when,"activity":i.activity,"data":i.data,"photo":i.photo,"like":i.like}
            activitydictlistmy.append(d)
        print(activitydictlistmy)

        return render(request,'profile.html',{"name":name,'profilepic':img,"email":inputemail,"friendlistemail":flistemail,"friendlistname":flistname,"friendlistpic":flistpic,"frienddictionary":frienddictlist,"list_reqfromemail":reqfromemail,"count_request":c,"activitydictlist":activitydictlist,"uploadedphotos":activitydictlistmy})
    except Exception as e1:
        print(e1)
        return render(request,'profile.html',{"name":name,'profilepic':None,"email":inputemail})

def search(request):
    if request.method=="POST":
        searchname=request.POST.get('searchname')
        #dbaccount=Account.objects.get(email=imail)
        #ifile=request.POST.get('inputfile')
        #ifile=request.FILES['inputfile']
        #print(type(ifile))
        #iabout=request.POST.get('inputabout')
        li=Account.objects.filter(name__icontains=searchname)
        #account1=Accountinfo(email=dbaccount,pic=ifile,about=iabout)
        #account1.save()
        #return render(request,'success.html',{"message":"congrats","name":searchname})
        inputemail=request.session['email']
        print("\n\n in search email=",inputemail,"\n\n")
        #flist=Friends.objects.filter(this_account=Account.objects.filter(email=inputemail)[0])
        flistemail=[]
        #for i in flist:
        #    flistemail.append(i.friend_account)
        flistemail=friend_email_get(inputemail)
        flistname=[]
        flistpic=[]
        for i in flistemail:
            x=Account.objects.filter(email=i)
            flistname.append(x[0].name)
            y=Accountinfo.objects.filter(email=x[0])
            if len(y) ==0:
                print("in if")     ######## 
                #print(y[0])
                flistpic.append("assets/uploaded_files/1429885540_94804_profile.jpg")
            else:
                print("in else")
                flistpic.append(y[0].pic)
        frienddictlist=[]
        for i in range(len(flistname)):
            d={'name':flistname[i],'email':flistemail[i],'pic':flistpic[i]}
            frienddictlist.append(d)
        print("\n\n changes made")
        req=FriendRequests.objects.filter(to_account=inputemail)
        print(req)
        reqfromemail=[]
        for i in req:
            x=i.from_account.email
            reqfromemail.append(x)
            print("\n\n\n i am about to send ")
        c=len(reqfromemail)
        print(c)  
        activitylist=[]
        for i in flistemail:
            o=Activity2.objects.filter(by=Account.objects.filter(email=i)[0])
            for j in o:
                activitylist.append(j)
                activitylist.sort(key=lambda x:x.when,reverse=True)
        activitydictlist=[]
        for i in range(len(activitylist)):
            d={"by":activitylist[i].by.email,"when":activitylist[i].when,"activity":activitylist[i].activity,"data":activitylist[i].data,"pic":activitylist[i].photo,"like":activitylist[i].like}
            print("\n",d,"\n")
            activitydictlist.append(d)
        print("activitydictlist",activitydictlist)
        activitydictlist=removeduplicate(activitydictlist)
        name=request.session['name']
        img=""
        try:
            a=Accountinfo.objects.filter(email=inputemail)
            if(len(a) == 0):
                img="assets/uploaded_files/1429885540_94804_profile.jpg"
            else:
                img=str(a[0].pic)
        except Exception as e:
            print(e)
            img=None
        a=Account.objects.get(email=inputemail)
        activity=[]
        try:
            activity=Activity2.objects.filter(by=a)
            print(a)
        except Exception as e:
            activity=[]
        activitydictlistmy=[]
        for i in activity:
            d={"when":i.when,"activity":i.activity,"data":i.data,"photo":i.photo,"like":i.like}
            activitydictlistmy.append(d)
            print(activitydictlistmy)
        activitydictlistmy=removeduplicate(activitydictlist)
      
        return render(request,'profile.html',{"name":name,'profilepic':img,"email":inputemail,"friendlistemail":flistemail,"friendlistname":flistname,"friendlistpic":flistpic,"frienddictionary":frienddictlist,"list_reqfromemail":reqfromemail,"count_request":c,"activitydictlist":activitydictlist,"searchresults":li,"uploadedphotos":activitydictlistmy})
        
def sendrequest(request):
    senderemail=request.session['email']
    r=friend_account1=request.get_full_path().split('/')[-2]
    reqtoemail=r[3:]
    from1=Account.objects.get(email=senderemail)
    a=FriendRequests(from_account=from1,to_account=reqtoemail)
    a.save()
    print("\n\n requested ")
    inputemail=request.session['email']
    #flist=Friends.objects.filter(this_account=Account.objects.filter(email=inputemail))
    flistemail=[]
    #for i in flist:
    #    flistemail.append(i.friend_account)
    flistemail=friend_email_get(inputemail)
    flistname=[]
    flistpic=[]
    for i in flistemail:
        x=Account.objects.filter(email=i)
        flistname.append(x[0].name)
        y=Accountinfo.objects.filter(email=x[0])
        if len(y) ==0:
                print("in if")     ######## 
                #print(y[0])
                flistpic.append("assets/uploaded_files/1429885540_94804_profile.jpg")
        else:
            print("in else")
            flistpic.append(y[0].pic)
    frienddictlist=[]
    for i in range(len(flistname)):
        d={'name':flistname[i],'email':flistemail[i],'pic':flistpic[i]}
        frienddictlist.append(d)
        print("\n\n changes made")
    frienddictlist=removeduplicate(frienddictlist)
    req=FriendRequests.objects.filter(to_account=inputemail)
    print(req)
    reqfromemail=[]
    for i in req:
        x=i.from_account.email
        reqfromemail.append(x)
    print("\n\n\n i am about to send ")
    c=len(reqfromemail)
    print(c)  
    activitylist=[]
    for i in flistemail:
        o=Activity2.objects.filter(by=Account.objects.filter(email=i))
        for j in o:
            activitylist.append(j)
    
    activitylist.sort(key=lambda x:x.when,reverse=True)
    activitydictlist=[]
    for i in range(len(activitylist)):
        d={"by":activitylist[i].by.email,"when":activitylist[i].when,"activity":activitylist[i].activity,"data":activitylist[i].data,"pic":activitylist[i].photo,"like":activitylist[i].like}
        print("\n",d,"\n")
        activitydictlist.append(d)
    print("activitydictlist",activitydictlist)
    activitydictlist=removeduplicate(activitydictlist)
    name=request.session['name']
    try:
        img=""
        a=Accountinfo.objects.filter(email=inputemail)
        if(len(a) == 0):
            img="assets/uploaded_files/1429885540_94804_profile.jpg"
        else:
            img=str(a[0].pic)
    except:
        img=None
    #### start
    a=Account.objects.get(email=inputemail)
    activity=[]
    try:
        activity=Activity2.objects.filter(by=a)
        print(a)
    except Exception as e:
        activity=[]
    activitydictlistmy=[]
    for i in activity:
        d={"when":i.when,"activity":i.activity,"data":i.data,"photo":i.photo,"like":i.like}
        activitydictlistmy.append(d)
    print(activitydictlistmy)
    activitydictlistmy=removeduplicate(activitydictlistmy)
    return render(request,'profile.html',{"name":name,'profilepic':img,"email":inputemail,"friendlistemail":flistemail,"friendlistname":flistname,"friendlistpic":flistpic,"frienddictionary":frienddictlist,"list_reqfromemail":reqfromemail,"count_request":c,"activitydictlist":activitydictlist,"uploadedphotos":activitydictlistmy})

    #return render(request,'success.html',{"message":"congrats","name":reqtoemail})

def uploadactivity(request):
    if request.method=="POST":
        imail=request.session['email']
        by1=Account.objects.filter(email=imail)[0]
        activity1=request.POST.get('activity')
        print(activity1)
        data1=request.POST.get('picdata')
        photo1=request.FILES['inputfile']
        a=Activity2(by=by1,activity=activity1,data=data1,photo=photo1,like=0)
        a.save()
        '''
        imail=request.POST.get('inputemail')
        dbaccount=Account.objects.get(email=imail)
        #ifile=request.POST.get('inputfile')
        ifile=request.FILES['inputfile']
        print(type(ifile))
        iabout=request.POST.get('inputabout')
        account1=Accountinfo(email=dbaccount,pic=ifile,about=iabout)
        account1.save()
        print(ifile)

        '''
        ##############
        inputemail=request.session['email']
        #flist=Friends.objects.filter(this_account=Account.objects.filter(email=inputemail)[0])
        flistemail=[]
        #for i in flist:
        #    flistemail.append(i.friend_account)
        flistemail=friend_email_get(inputemail)
        flistname=[]
        flistpic=[]
        for i in flistemail:
            x=Account.objects.filter(email=i)
            flistname.append(x[0].name)
            y=Accountinfo.objects.filter(email=x[0])
            if len(y) ==0:
                print("in if")     ######## 
                #print(y[0])
                flistpic.append("assets/uploaded_files/1429885540_94804_profile.jpg")
            else:
                print("in else")
                flistpic.append(y[0].pic)
        
        frienddictlist=[]
        for i in range(len(flistname)):
            d={'name':flistname[i],'email':flistemail[i],'pic':flistpic[i]}
            frienddictlist.append(d)
            print("\n\n changes made")
        req=FriendRequests.objects.filter(to_account=inputemail)
        frienddictlist=removeduplicate(frienddictlist)
        print(req)
        reqfromemail=[]
        for i in req:
            x=i.from_account.email
            reqfromemail.append(x)
        print("\n\n\n i am about to send ")
        c=len(reqfromemail)
        print(c)  
        activitylist=[]
        for i in flistemail:
            o=Activity2.objects.filter(by=Account.objects.filter(email=i)[0])
            for j in o:
                activitylist.append(j)
        activitylist.sort(key=lambda x:x.when,reverse=True)
        
        activitydictlist=[]
        for i in range(len(activitylist)):
            d={"by":activitylist[i].by.email,"when":activitylist[i].when,"activity":activitylist[i].activity,"data":activitylist[i].data,"pic":activitylist[i].photo,"like":activitylist[i].like}
            print("\n",d,"\n")
            activitydictlist.append(d)
        print("activitydictlist",activitydictlist)
        activitydictlist=removeduplicate(activitydictlist)
        name=request.session['name']
        try:
            img=""
            a=Accountinfo.objects.filter(email=inputemail)
            if(len(a) == 0):
                img="assets/uploaded_files/1429885540_94804_profile.jpg"
            else:
                img=str(a[0].pic)
        except Exception as e:
            print(e)
            img=None
        #### start
        a=Account.objects.get(email=inputemail)
        activity=[]
        try:
            activity=Activity2.objects.filter(by=a)
            print(a)
        except Exception as e:
            print(e)
            activity=[]
        activitydictlistmy=[]
        for i in activity:
            d={"when":i.when,"activity":i.activity,"data":i.data,"photo":i.photo,"like":i.like}
            activitydictlistmy.append(d)
        print(activitydictlistmy)
        return render(request,'profile.html',{"name":name,'profilepic':img,"email":inputemail,"friendlistemail":flistemail,"friendlistname":flistname,"friendlistpic":flistpic,"frienddictionary":frienddictlist,"list_reqfromemail":reqfromemail,"count_request":c,"activitydictlist":activitydictlist,"uploadedphotos":activitydictlistmy})


        #return render(request,'success.html',{"message":"congrats","name":imail})


        








