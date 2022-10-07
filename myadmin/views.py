from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from myproject import models as myproject_models
from . import models


#middleware to check session for admin routes
def sessioncheckmyadmin_middleware(get_response):
	def middleware(request):
		if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/':
			if request.session['sunm']==None or request.session['srole']!="admin":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware



# Create your views here.

def adminhome(request):
	return render(request,"adminhome.html",{"sunm":request.session['sunm']})         

def manageusers(request):
    userDetails=myproject_models.Register.objects.filter(role='user')
    return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session['sunm']})

def manageuserstatus(request):
    regid=request.GET.get("regid")    
    s=request.GET.get("s")
    
    if s=="block":
        myproject_models.Register.objects.filter(regid=int(regid)).update(status=0)    
    elif s=="verify":
        myproject_models.Register.objects.filter(regid=int(regid)).update(status=1)
    else:
        myproject_models.Register.objects.filter(regid=int(regid)).delete()
    return redirect("/myadmin/manageusers/")


def addcategory(request):
    if request.method=="GET":
        return render(request,"addcategory.html",{'output':'',"sunm":request.session['sunm']})
    else:
        catnm=request.POST.get('catnm')
        caticon=request.FILES['caticon']
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.Category(catnm=catnm,caticonnm=filename)
        p.save()
        return render(request,"addcategory.html",{'output':'Category added successfully',"sunm":request.session['sunm']})


def addsubcategory(request):
    clist=models.Category.objects.all()    
    if request.method=="GET":
        return render(request,"addsubcategory.html",{'output':'','clist':clist,"sunm":request.session['sunm']})
    else:
        catnm=request.POST.get('catnm')
        subcatnm=request.POST.get('subcatnm')
        caticon=request.FILES['caticon']
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.SubCategory(catnm=catnm,subcatnm=subcatnm,subcaticonnm=filename)
        p.save()
        return render(request,"addsubcategory.html",{'output':'SubCategory added successfully','clist':clist,"sunm":request.session['sunm']})        
        
def cpadmin(request):
	if request.method=="GET":
		return render(request,"cpadmin.html",{"sunm":request.session['sunm'],"output":""})         
	else:
		opass=request.POST.get('opass')
		npass=request.POST.get('npass')
		cnpass=request.POST.get('cnpass')
		
		userDetails=myproject_models.Register.objects.filter(username=request.session['sunm'],password=opass)		
		
		if len(userDetails)==0:
			msg="Invalid old password , please try again"
		else:
			if npass==cnpass:
				myproject_models.Register.objects.filter(username=request.session['sunm'],password=opass).update(password=cnpass)
				msg="Password updated successfully , please login again"					
			else:
				msg="New & Confirm new password not matched"		
		return render(request,"cpadmin.html",{"sunm":request.session['sunm'],"output":msg})
			
	
def epadmin(request):
	userDetails=myproject_models.Register.objects.filter(username=request.session['sunm'])		

	m,f="",""
	if userDetails[0].gender=="male":
		m="checked"
	else:
		f="checked"	
	
	if request.method=="GET":
		if request.GET.get("s")==None:
			msg=""
		else:
			msg="Profile updated successfully...."	
		return render(request,"epadmin.html",{"userDetails":userDetails[0],"m":m,"f":f,"sunm":request.session['sunm'],"msg":msg})
	else:
		name=request.POST.get("name")
		username=request.POST.get("username")
		address=request.POST.get("address")
		mobile=request.POST.get("mobile")
		city=request.POST.get("city")
		gender=request.POST.get("gender")
		
		myproject_models.Register.objects.filter(username=username).update(name=name,address=address,mobile=mobile,city=city,gender=gender)
		
		return redirect('/myadmin/epadmin/?s=True')		
	
	
	
	
	
	
	
	
	
	       	
	
