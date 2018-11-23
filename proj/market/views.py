from .models import Post,Customer
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import send_mail
# Create your views here.

def stuff(request):

    posts = Post.objects.all()
    return render(request, 'market/stuff.html', {})

@login_required(login_url='/market/signup')	
def cart(request):
	cust=Customer.objects.get(user=request.user)
	p=cust.book.all()
	response={}
	response['ebook']=p
	count=0
	c=0
	for k in p:
		count=count+1
		c=c+k.cost
	response['count']=count
	response['c']=c
	return render(request, 'market/cart.html', response)

@login_required(login_url='/market/signup')	
def about(request):
    return render(request, 'market/about.html', {})


def signup(request):
	response = {}
	if request.method == 'POST' :
		username = request.POST['username']
		password = request.POST['password']
		if User.objects.filter(username=username):
			response['error']=1
		else:
			User.objects.create_user(username = username,password = password,email='')
			cust=Customer()
			cust.user=User.objects.get(username=username)
			cust.save()
	return render(request,'market/login.html',response)



def signin(request):
	response = {}
	if request.method == 'POST' :
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is None :
			response['error']=2
			return render(request,'market/login.html',response)
		else :
			login(request,user)
			return redirect('/market/index/')
	return render(request,'market/login.html',response)

@login_required(login_url='/market/signup')
def index(request):

    posts = Post.objects.all()
    response={}
    response['posts']=posts
    cust=Customer.objects.get(user=request.user)
    response['user']=request.user
    p=cust.book.all()
    count=0
    c=0
    for k in p:
    	count=count+1
    	c=c+k.cost
    response['count']=count
    response['c']=c
    response['ebook']=p
    return render(request, 'market/index.html', response)

@login_required(login_url='/market/signup')
def addtocart(request,post):
	p=Post.objects.get(title=post)
	cust=Customer.objects.get(user=request.user)
	cust.book.add(p)
	cust.save()
	return redirect('/market/index')

@login_required(login_url='/market/signup')
def delfromcart(request,post):
    p=Post.objects.get(title=post)
    cust=Customer.objects.get(user=request.user)
    cust.book.delete(p);
    cust.save()
    return redirect('/market/index')


@login_required(login_url='/market/signup')
def logout_view(request):
	logout(request)
	return redirect('/market/signup')



@login_required(login_url='/market/signup')
def booklist(request):

	if request.method == 'POST' :
		eb = request.POST['ebook']
		ty = request.POST['type']
		#vl=request.POST['value-lower']
		#vu=request.POST['value-upper']
		#print vl
		#print vu
		prod = Post.objects.all()
		posts=[]
		for pr in prod:
			if ty=="title" and eb.lower() in pr.title.lower():
				posts.append(pr)
			if ty=="author" and eb.lower() in pr.author.username.lower():
				posts.append(pr)
			if ty=="dop" and eb == pr.pub_date.isoformat():
				posts.append(pr)
	else:
		posts = Post.objects.all()
    
	response={}
	response['posts']=posts
	cust=Customer.objects.get(user=request.user)
	response['user']=request.user
	p=cust.book.all()
	count=0
	c=0
	for k in p:
		count=count+1
		c=c+k.cost
	response['count']=count
	response['c']=c
	response['ebook']=p
	return render(request, 'market/ebook.html', response)
