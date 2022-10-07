from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.conf import settings
from . import emailAPI   

import time
from . import models
from myadmin import models as myadmin_models

media_url=settings.MEDIA_URL

#middleware to check session for mainapp routes
def sessioncheck_middleware(get_response):
	def middleware(request):
		if request.path=='' or request.path=='/home/' or request.path=='/about/' or request.path=='/contact/' or request.path=='/login/' or request.path=='/service/' or request.path=='/register/':
			request.session['sunm']=None
			request.session['srole']=None
			
			response = get_response(request)
				
		else:
			response = get_response(request)		
		return response	
	return middleware


def home(request):
    clist=myadmin_models.Category.objects.all()
    return render(request,"home.html",{"clist":clist,"media_url":media_url})

def viewsubcat(request):
    catnm=request.GET.get('cnm')
    sclist=myadmin_models.SubCategory.objects.filter(catnm=catnm)
    clist=myadmin_models.Category.objects.all()
    return render(request,"viewsubcat.html",{"clist":clist,"sclist":sclist,"media_url":media_url,"catnm":catnm})

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def service(request):
    return render(request,"service.html")

def register(request):
    if request.method=="GET":
        return render(request,"register.html",{"msg":""})
    else:
        #to recieve data on views from form
        #print(request.POST)
        name=request.POST.get("name")
        username=request.POST.get("username")
        password=request.POST.get("password")
        address=request.POST.get("address")
        mobile=request.POST.get("mobile")
        city=request.POST.get("city")
        gender=request.POST.get("gender")
        info=time.asctime()

        p=models.Register(name=name,username=username,password=password,address=address,mobile=mobile,city=city,gender=gender,role="user",status=0,info=info)
        p.save()
        
        emailAPI.sendMail(username,password)

        return render(request,"register.html",{"msg":"User registered successfully...."})    
        
        
def verify(request):
	vemail=request.GET.get("vemail")
	models.Register.objects.filter(username=vemail).update(status=1)			
	return redirect('/login/')        
        
def checkEmail(request):
	unm=request.GET.get('unm')
	
	userDetails=models.Register.objects.filter(username__startswith=unm)
	
	if len(userDetails)==0:
		res=0
	else:
		res=1		
	return HttpResponse(res)        
        

def login(request):
	cunm,cpass="",""
	if request.COOKIES.get('cunm')!=None:
		cunm=request.COOKIES.get('cunm')	
		cpass=request.COOKIES.get('cpass')

	if request.method=="GET":
		return render(request,"login.html",{"msg":"",'cunm':cunm,'cpass':cpass})
	else:        
		username=request.POST.get("username")
		password=request.POST.get("password")
		userDetails=models.Register.objects.filter(username=username,password=password,status=1)                    
        
		if len(userDetails)==0:
			return render(request,"login.html",{"msg":"Invalid user or verify your account....",'cunm':cunm,'cpass':cpass})
		else:
			# Session to store user details
			request.session['sunm']=userDetails[0].username 
			request.session['srole']=userDetails[0].role
			
			if userDetails[0].role=="user":
				response=redirect("/user/")
			else:
				response=redirect("/myadmin/")
			
			#to store user details in cookies
			if request.POST.get('chk')!=None:
				response.set_cookie("cunm",userDetails[0].username,3600*24)
				response.set_cookie("cpass",userDetails[0].password,3600*24)

			return response	        
                
                
                
