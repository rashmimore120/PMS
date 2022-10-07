from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
import time

#middleware to check session for user routes
def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/':
			if request.session['sunm']==None or request.session['srole']!="user":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware


# Create your views here.

def userhome(request):
    return render(request,"userhome.html",{"sunm":request.session['sunm']})
    
def funds(request):
	PAYPAL_URL="https://www.sandbox.paypal.com/cgi-bin/webscr"
	PAYPAL_ID="sb-tuesq8599991@business.example.com"
	#personal : sb-cidti8639496@personal.example.com
	return render(request,"funds.html",{"sunm":request.session['sunm'],"PAYPAL_URL":PAYPAL_URL,"PAYPAL_ID":PAYPAL_ID})             
	
def payment(request):
	uid=request.GET.get('uid')
	amount=request.GET.get('amount')
	info=time.asctime()
	
	p=models.Payment(uid=uid,amount=amount,info=info)	
	
	p.save()
	
	return redirect('/user/success/')
    
def success(request):
    return render(request,"success.html",{"sunm":request.session['sunm']})
    
def cancel(request):
    return render(request,"cancel.html",{"sunm":request.session['sunm']})        
    	
