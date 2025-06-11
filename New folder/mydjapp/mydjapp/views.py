from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from  . import models
from . import emailAPI
import time

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def service(request):
    return render(request,"service.html")

def register(request):
    if request.method=="GET":
        return render(request,"register.html",{"output":""})
    else:
        #to recieve data from UI 'form'
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        #to insert record in database using models
        p=models.Register(name=name,email=email,password=password,mobile=mobile,address=address,city=city,gender=gender,status=0,role="user",info=time.asctime())
        p.save()

        #to integrate EmailAPI 
        emailAPI.sendMail(email,password)

        return render(request,"register.html",{"output":"User register successfully...."})    


def login(request):
    if request.method=="GET":    
        return render(request,"login.html",{"output":""})
    else:
        #to recieve data from UI 'form'
        email=request.POST.get("email")
        password=request.POST.get("password")

        #to check record in database
        userDetails=models.Register.objects.filter(email=email,password=password,status=1)

        if len(userDetails)>0:

            request.session['sunm']=userDetails[0].email
            request.session['srole']=userDetails[0].role        

            #print(userDetails[0].role) #to get user role
            if userDetails[0].role=="admin":
                return redirect("/myadmin/")
            else:    
                return redirect("/user/")
        else:
            return render(request,"login.html",{"output":"Invalid user or verify your account...."})            


def verify(request):
    vemail=request.GET.get("vemail")
    models.Register.objects.filter(email=vemail).update(status=1)
    return redirect("/register/")

def adminhome(request):
    return render(request,"adminhome.html",{"sunm":request.session["sunm"]})

def manageusers(request):
    userDetails=models.Register.objects.filter(role="user")
    return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session["sunm"]})    

def manageuserstatus(request):
    #to get data from url
    s=request.GET.get("s")
    regid=int(request.GET.get("regid"))

    if s=="active":
        models.Register.objects.filter(regid=regid).update(status=1)
    elif s=="inactive":
        models.Register.objects.filter(regid=regid).update(status=0)
    else:
        models.Register.objects.filter(regid=regid).delete()
                    

    return redirect("/manageusers/")

def userhome(request):
    return render(request,"userhome.html",{"sunm":request.session["sunm"]})

def sharenotes(request):
    if request.method=="GET":
        return render(request,"sharenotes.html",{"sunm":request.session["sunm"],"output":""})
    else:

        #to recieve data from ui
        title=request.POST.get("title")
        category=request.POST.get("category")
        description=request.POST.get("description")

        #to recive file & to push file in media folder
        file=request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(file.name,file)

        p=models.sharenotes(title=title,category=category,decription=description,filename=filename,uid=request.session["sunm"],info=time.asctime())
        p.save()

        return render(request,"sharenotes.html",{"sunm":request.session["sunm"],"output":"Content uploaded successfully....."})                

def viewnotes(request):
    data=models.sharenotes.objects.all()
    return render(request,"viewnotes.html",{"sunm":request.session["sunm"],"data":data})

def funds(request):
    paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
    #sb-r2nzw43244614@personal.example.com
    #8Z}>jY.R
    paypalID="sb-l34s943008264@business.example.com"
    amt=100
    return render(request,"funds.html",{"paypalURL":paypalURL,"paypalID":paypalID,"amt":amt,"sunm":request.session["sunm"]})

def payment(request):
    return redirect("/success/")

def success(request):
    return render(request,"success.html",{"sunm":request.session.get('sunm')})

def cancel(request):
    return render(request,"cancel.html",{"sunm":request.session["sunm"]})

def cpadmin(request):
    email=request.session["sunm"]
    if request.method=="GET":
        return render(request,"cpadmin.html",{"sunm":email,"output":""})
    else:
        opassword=request.POST.get("opassword")
        npassword=request.POST.get("npassword")
        cnpassword=request.POST.get("cnpassword")        

        userDetails=models.Register.objects.filter(email=email,password=opassword)
        if len(userDetails)>0:
            if npassword==cnpassword:
                models.Register.objects.filter(email=email).update(password=cnpassword)
                msg="Password changed successfully...."        
            else:
                msg="New & Confirm new password mismatch...."             
        else:
            msg="Invalid old password , please try again...."    
        return render(request,"cpadmin.html",{"sunm":email,"output":msg})


def cpuser(request):
    email=request.session["sunm"]
    if request.method=="GET":
        return render(request,"cpuser.html",{"sunm":email,"output":""})
    else:
        opassword=request.POST.get("opassword")
        npassword=request.POST.get("npassword")
        cnpassword=request.POST.get("cnpassword")        

        userDetails=models.Register.objects.filter(email=email,password=opassword)
        if len(userDetails)>0:
            if npassword==cnpassword:
                models.Register.objects.filter(email=email).update(password=cnpassword)
                msg="Password changed successfully...."        
            else:
                msg="New & Confirm new password mismatch...."             
        else:
            msg="Invalid old password , please try again...."    
        return render(request,"cpuser.html",{"sunm":email,"output":msg})




def epadmin(request):
    
    email=request.session["sunm"]
    models.Register.object.filter(email=email)
    if request.method=="GET":
        return render(request,"epadmin.html",{"sunm":email,"user":userDetails[0]})
        print(userDetails)
    else:
        opassword=request.POST.get("opassword")
        npassword=request.POST.get("npassword")
        cnpassword=request.POST.get("cnpassword")        

        userDetails=models.Register.objects.filter(email=email,password=opassword)
        if len(userDetails)>0:
            if npassword==cnpassword:
                models.Register.objects.filter(email=email).update(password=cnpassword)
                msg="profile edit succesfully...."        
            else:
                msg="New & Confirm new password mismatch...."             
        else:
            msg="Invalid old password , please try again...."    
        return render(request,"epadmin.html",{"sunm":email,"output":msg})
