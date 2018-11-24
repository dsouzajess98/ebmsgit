from .models import *
from .render import *
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.core.files.storage import FileSystemStorage
from zipfile import ZipFile
import glob
import os

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
	response['flag1']=1
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

def sendemail(request):
	subject = 'Thank you for registering to our site'
	message = ' it  means a world to us '
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [request.user.email,]
	send_mail( subject, message, email_from, recipient_list )

def preview(request):
	#template=get_template('printpreview.html')
	#return HttpResponse("Hello")
	template=get_template('printpreview.html')
	#print template
	cust=Customer.objects.get(user=request.user)
	p=cust.book.all()
	context={}
	context['name']=request.user.username
	context['ebook']=p
	html=template.render(context)
	pdf=render_to_pdf('printpreview.html',context)
	return HttpResponse(pdf,content_type='application/pdf')



 
def merger(request):
	pdf_writer = PdfFileWriter()
	cust=Customer.objects.get(user=request.user)
	p=cust.book.all()	
	for path in p:
		ps=os.path.join(settings.MEDIA_ROOT,path.file.url.replace(settings.MEDIA_URL,""))
		ps=ps.replace("/","\\")
		ps=ps.replace("%20"," ")
		#print ps
		pdf_reader = PdfFileReader(ps)
		for page in range(pdf_reader.getNumPages()):
			pdf_writer.addPage(pdf_reader.getPage(page))
	op=os.path.join(settings.MEDIA_ROOT,'zj.pdf')
	print op

	fs=FileSystemStorage()
	with fs.open(op,'wb') as fh:
	    pdf_writer.write(fh)
	with fs.open(op) as pdf:
	    response=HttpResponse(pdf,content_type='application/pdf')
	    #response['Content-Disposition']='inline; filename="zj.pdf"'
	    return response
	#fd=open(fh,'r')	

	return HttpResponse("sdad")

def zipmerger(request):
	cust=Customer.objects.get(user=request.user)
	p=cust.book.all()
	with ZipFile('my_python_files.zip','w') as zip: 
        # writing each file one by one 
		for path in p:
			ps=os.path.join(settings.MEDIA_ROOT,path.file.url.replace(settings.MEDIA_URL,""))
			ps=ps.replace("/","\\")
			ps=ps.replace("%20"," ")
			zip.write(ps)
			
	response=HttpResponse(open('my_python_files.zip'),content_type='application/zip')
	response['Content-Disposition']='attachment; filename="ebook.zip"'
	return response

def ebook_view(request,item):
	response={}
	response['item']=item
	p=Post.objects.get(title=item)
	response['comm']=p.comments.all()
	cnt=0
	for v in p.comments.all():
		cnt=cnt+1
	chk=p.tags.all()
	response['tags']=chk
	reltag=[]
	for g in Post.objects.exclude(title=item):
		for t in p.tags.all():
			if g.tags.filter(tag_name=t.tag_name).exists():
				reltag.append(g)
				break	
		
	response['rel']=reltag
	response['cnt']=cnt
	response['post']=p
	response['user']=request.user
	cust=Customer.objects.get(user=request.user)
	p1=cust.book.all()

	count=0
	c=0
	for k in p1:
		count=count+1
		c=c+k.cost
	response['count']=count
	response['c']=c
	response['ebook']=p1

	return render(request,'market/product-detail.html',response)


def addcomment(request,item):
	if request.method == 'POST' :
		comm = request.POST['comment']
		p=Post.objects.get(title=item)
		c=Comment()
		c.text=comm
		c.user=request.user
		c.save()
		p.comments.add(c)
		p.save()
		st='/market/ebook/'+item
	return redirect(st)	


def category(request,cat):
	prod = Post.objects.all()
	posts=[]
	for pr in prod:
		if pr.tags.filter(tag_name=cat).exists():
			posts.append(pr)
    
	response={}
	response['posts']=posts
	cust=Customer.objects.get(user=request.user)
	response['user']=request.user
	if cat == 'New':
		response['flag1']=2
	elif cat =='Best Seller':
		response['flag1']=3
	elif cat =='Classic':
		response['flag1']=4
	elif cat =='Educational':
		response['flag1']=5
	else:
		response['flag1']=6
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


