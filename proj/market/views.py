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
from django.core.mail import send_mail, EmailMessage
import mimetypes
from django.contrib.admin.views.decorators import staff_member_required,user_passes_test

# Create your views here.

def stuff(request):

    posts = Post.objects.all()
    return render(request, 'market/stuff.html', {})

@login_required(login_url='/market/signup')	
def payment(request):

    return render(request, 'market/payment.html', {})

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

@login_required(login_url='/market/signup')	
def admin_add(request):
	cust=Customer.objects.get(user=request.user)
	if cust.is_priv:
		return render(request, 'market/admin_add.html', {})
	else:
		return redirect('/market/signup')

@login_required(login_url='/market/signup')	
def admin_remove(request,post):
	cust=Customer.objects.get(user=request.user)
	if cust.is_priv:
		Post.objects.filter(title=post).delete()
		return redirect('/market/admin')
	else:
		return redirect('/market/signup')

@login_required(login_url='/market/signup')	
def removeuser(request,post):
	if request.user.is_superuser:
		user=User.objects.get(username=post)
		Customer.objects.filter(user=user).delete()
		User.objects.filter(username=post).delete()
		return redirect('/market/admin')
	else:
		return redirect('/market/signup')

@login_required(login_url='/market/signup')	
def admin(request):
	if not request.user.is_authenticated():
		return redirect('/market/signup')
	cust=Customer.objects.get(user=request.user)
	flag=0
	user=[]
	if request.user.is_superuser:
		flag=1
		user=Customer.objects.all()
	if cust.is_priv:
		post=Post.objects.all()
		response={}
		response['posts']=post
		response['flag']=flag
		response['cust']=user
		return render(request, 'market/admin.html', response)
	else:
		return redirect('/market/signup')

def give_priv(request,un):
	user=User.objects.get(username=un)
	cust=Customer.objects.get(user=user)
	cust.is_priv=True
	cust.save()
	return redirect('/market/admin')

def saveData(request):
	if request.method == "POST" :
		title = request.POST['title']
		desc = request.POST['description']
		cost = request.POST['cost']
		dop = request.POST['dop']
		image = request.FILES['image']
		file = request.FILES['file']
		other=request.FILES.getlist('otherfiles')
		obj = Post()
		obj.title=title
		obj.desc=desc
		obj.cost=cost
		obj.author=request.user
		obj.pub_date=dop
		obj.file=file
		obj.image=image
		obj.save()
		tags=request.POST.getlist('tag')
		for t in tags:
			t1=Tag.objects.get(tag_name=t)
			print t
			obj.tags.add(t1)
			obj.save()
		
		for a in other:
			f=FileUpload()
			f.file_type=a.content_type
			f.file=a
			f.title=title
			f.save()
			obj.otherformat.add(f)

		obj.save()
		
	return redirect('/market/admin')

def signup(request):
	response = {}
	if request.method == 'POST' :
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		if User.objects.filter(username=username):
			response['error']=1
		else:
			User.objects.create_user(username = username,password = password,email = email)
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
		response['flag']=1
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
def delfromcart(request,post):
    p=Post.objects.get(title=post)
    cust=Customer.objects.get(user=request.user)
    cust.book.filter(title=post).delete();
    cust.save()
    return redirect('/market/cart')


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
			elif ty=="author" and eb.lower() in pr.author.username.lower():
				posts.append(pr)
			elif ty=="dop" and eb == pr.pub_date.isoformat():
				posts.append(pr)
			elif ty=="isbn":
				template="https://isbndb.com/book/"
				template+=eb
				return redirect(template)	
			elif ty=="comment":
				for c in pr.comments.all():
					if eb.lower() in c.text.lower():
						posts.append(pr)
						break
			elif ty=="edition" and eb.lower() in pr.edition.lower():
				posts.append(pr)
			elif ty=="series" and eb.lower() in pr.series.lower():
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
		pts=[]
		c=0
		for p in Post.objects.all():
			ps=os.path.join(settings.MEDIA_ROOT,p.file.url.replace(settings.MEDIA_URL,""))
			ps=ps.replace("/","\\")
			ps=ps.replace("%20"," ")
			size=os.path.getsize(ps)
			resp={}
			resp['file']=p
			resp['size']=size
			pts.append(resp)
		pts = sorted(pts, key = lambda i: i['size']) 
		print pts
		posts=[]
		for p in pts:
			posts.append(p['file'])

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

def userdetails(request,un):
	response={}
	response['un']=un
	user=User.objects.get(username=un)
	p=Customer.objects.get(user=user)
	response['p']=user
	response['book']=p.book.all()
	response['user']=request.user
	response['pr']=p.is_priv
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

	return render(request,'market/user-detail.html',response)

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

