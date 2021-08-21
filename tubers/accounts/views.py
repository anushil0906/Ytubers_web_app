from django.shortcuts import redirect,render
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
import re
from django.contrib import auth
from django.contrib import messages 


# Create your views here.

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		string_check= re.compile('[\'=!"%^&*()<>?/\|}{~:]')

		user = auth.authenticate(username=username,password=password)

		if user is not None and  string_check.search(username) == None and string_check.search(password) == None:
			auth.login(request,user)
			messages.success(request,'you are logged in')
			return redirect('dashboard')
		elif user is  None and  string_check.search(username) != None or string_check.search(password) != None:
			messages.warning(request,'invalid creds and SQL INJECTION are not allowed')
			return redirect('login')
		else:
		    messages.warning(request,'invalid credentials')
		    return redirect('login')	
	return render(request,'accounts/login.html')


def register(request):
	
	if request.method == 'POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		confirm_password = request.POST['confirm_password']

		string_check= re.compile('[\'=!"%^&*()<>?/\|}{~:]')


		if (password == confirm_password) and (string_check.search(firstname) == None) and (string_check.search(lastname) == None) and (string_check.search(username) == None) and (string_check.search(email) == None) and (string_check.search(password) == None) :

			
			if User.objects.filter(username=username).exists():
				messages.warning(request,'username exists')
				return redirect('register')
			
			else:
				
				if User.objects.filter(email=email).exists():
					messages.warning(request,'email exists')
					return redirect('register')
				
				else:
				    user = User.objects.create_user(
				    	first_name=firstname,last_name=lastname,username=username,email=email,password=password)
				    user.save()
				    messages.success(request,"Account is register successfully")
				    return redirect('login')
			    

		elif (string_check.search(firstname) != None) or  (string_check.search(lastname) != None) or  (string_check.search(username) != None) or  (string_check.search(email) != None)  or (string_check.search(password) != None) :

		    messages.warning(request,"special characters are not allowed")
		else :
			messages.warning(request,"password not match")
		    	

		
	return render(request,'accounts/register.html')

def logouts(request):
	logout(request)
	return redirect('home')

@login_required(login_url='login')
def dashboard(request):
	return render(request,'accounts/dashboard.html')	