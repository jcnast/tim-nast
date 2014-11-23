from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
import simplejson
from requests import get

url = 'http://api.soundcloud.com/users/tim-nast/tracks.json?client_id=eefc5d8629bc73f7a72c3af35b62bc64'
def soundcloud_api():
	data = simplejson.loads(get('%s' % url, verify=False).text)
	return data

def home(request):
	user= 'False'
	if request.user.is_authenticated():
		user = 'True'

	data = soundcloud_api() # get all information about all tracks
	data.sort(key=lambda item:item['created_at'], reverse=True) # order tracks by release data

	latest_track = data[0]

	context = {'user': user, 'latest_track': latest_track}
	return render(request, 'welcome-page.html', context)

def bio(request):
	user= 'False'
	if request.user.is_authenticated():
		user = 'True'

	data = soundcloud_api() # get all information about all tracks
	data.sort(key=lambda item:item['created_at'], reverse=True) # order tracks by release data

	latest_track = data[0]

	context = {'user': user, 'latest_track': latest_track}
	return render(request, 'bio.html', context)

def sign_in(request):

	if request.method=='POST':
		#gets the username and password
		username = request.POST['username']
		password = request.POST['password']
		#tries authenticate the user
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				#if allowed, the user is logged in
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				#otherwise the user is told they cant log in
				return render(request, 'sign-in.html', {'error': 'User is unable to login'})
		else:
			#user is told they cant log in
			return render(request, 'sign-in.html', {'error': 'Failed to login'})
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return render(request, 'sign-in.html')

@login_required
def sign_out(request):
	logout(request)
	return HttpResponseRedirect('/')

def sign_up(request):

	if request.method=='POST':
		print request.POST
		#gets the username and password and email
		username = request.POST['username']
		password = request.POST['password']
		cpassword = request.POST['confirmPassword']
		email = request.POST['email']
		# makes the user if it can
		if username != '':
			if not(User.objects.filter(username=username)):
				if password == cpassword:
					if password:
						user = User.objects.create_user(username=username, password=password, email=email)
						user = authenticate(username=username, password=password)
					else:
						return render(request, 'sign-up.html', {'error': 'No password given', 'info': request.POST})
				else:
					return render(request, 'sign-up.html', {'error': 'Passwords did not match', 'info': request.POST})
			else:
				return render(request, 'sign-up.html', {'error': 'Username is taken', 'info': request.POST})
		else:
			return render(request, 'sign-up.html', {'error': 'No username was given', 'info': request.POST})
		
		if user is not None:
			if user.is_active:
				#if allowed, the user is logged in
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				#otherwise the user is told they cant log in
				return render(request, 'sign-up.html', {'error': 'User is unable to login'})
		else:
			#user is told they cant log in
			return render(request, 'sign-up.html', {'error': 'Failed to login'})
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return render(request, 'sign-up.html')