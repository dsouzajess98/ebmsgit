from .models import Post,Customer
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import send_mail, EmailMessage
import mimetypes
from django.contrib.admin.views.decorators import staff_member_required,user_passes_test
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

def about(request):
    return render(request, 'market/about.html', {})

@user_passes_test(lambda u: u.is_superuser)
def admin_add(request):
    return render(request, 'market/admin_add.html', {})

@user_passes_test(lambda u: u.is_superuser)
def admin_remove(request,post):
	Post.objects.filter(title=post).delete()
    return redirect('/market/admin')

@user_passes_test(lambda u: u.is_superuser)
def admin(request):
	print(******************)
	print(request.user.is_staff)
	if request.user.is_staff and request.user.is_superuser :
		post=Post.objects.all()
		response={}
		response['posts']=post
		return render(request, 'market/admin.html', response)
	else:
		return redirect('/market/signup')

def saveData(request):
	if request.method == "POST" :
		title = request.POST['title']
		desc = request.POST['description']
		cost = request.POST['cost']
		dop = request.POST['dop']
		image = request.POST['image']
		file = request.POST['file']
		obj = Post()
		obj.title=title
		obj.desc=desc
		obj.cost=cost
		obj.author=request.user
		obj.pub_date=dop
		obj.file=file
		obj.image=image
		obj.save()
		
	return redirect('/market/admin')

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

def index(request):

    posts = Post.objects.all()
    response={}
    response['posts']=posts
    if not request.user.is_authenticated():
		return render(request,'market/index.html',response)
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
	c=0
	p.count=p.count+1
	p.save()
	print p.count
	p=Post.objects.all()
	print p
	for po in p:
		c=c+po.count
	print c
	for po in p:
		c1=po.count/c
		if c1>=0.8:
			po.rating=5
		elif c1>=0.6:
			po.rating=4
		elif c1>=0.4:
			po.rating=3
		elif c1>=0.2:
			po.rating=2
		else:
			po.rating=1
		po.save()
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
	

def sort(request,ty):
	posts=[]
	#if request.method == 'POST' :
	#ty = request.POST.get('sorting')
	print ty
	if ty=="author":
		posts=Post.objects.all().order_by("author")
	elif ty=="priceasc":
		posts=Post.objects.all().order_by("cost")
	elif ty=="pricedesc":
		posts=Post.objects.all().order_by("-cost")
	elif ty=="title":
		posts=Post.objects.all().order_by("title")
	elif ty=="pubdate":
		posts=Post.objects.all().order_by("pub_date")
	elif ty=="rating":
		posts=Post.objects.all().order_by("-rating")
	elif ty=="size":
		posts=Post.objects.all()
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
	
def news(request):
	if not request.user.is_authenticated():
		return render(request,'market/news.html',{})
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
	return render(request, 'market/news.html', response)
	

def checkout(request):
	if not request.user.is_authenticated():
		return render(request,'market/news.html',{})
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
	return render(request, 'market/checkout.html', response)

def send_mail(request):
	cust=Customer.objects.get(user=request.user)
	p=cust.book.all()
	mail = EmailMessage("Ebooks", "", "seproj123@gmail.com", [request.user.email])
	for k in p:
		#f=open(k.file.name)
		content_type= mimetypes.guess_type(k.file.name)[0]
		#print content_type
		mail.attach(k.file.name,k.file.read(),content_type)
	mail.send()
	return redirect('/market/checkout')