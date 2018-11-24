from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        url(r'^$', views.stuff, name='stuff'),
        url(r'^signup/$', views.signup, name='signup'),
        url(r'^login/$', views.signin, name='login'),
		url(r'^cart/$', views.cart, name='cart'),
		url(r'^about/$', views.about, name='about'),
		url(r'^index/$', views.index, name='index'),
        url(r'^booklist/$', views.booklist, name='index'),
        url(r'^addtocart/(?P<post>[A-Za-z0-9., ]+)/$', views.addtocart, name='addtocart'),
        url(r'^logout/$',views.logout_view,name="logout"),
        url(r'^news/$', views.news, name='news'),
        url(r'^checkout/$', views.checkout, name='checkout'),
        #url(r'^sendemail/$', views.sendemail, name='sendemail'),
        #url(r'^pdf-viewer/$', views.pdf_viewer, name='pdf_viewer_page'),
        url(r'^pdf/$', views.merger, name='pdf_viewer_page'),
        url(r'^ebook/(?P<item>[A-Za-z0-9., ]+)/$', views.ebook_view, name='ebook-view'),
        url(r'^addcomment/(?P<item>[A-Za-z0-9., ]+)/$', views.addcomment, name='addcomment'),
        url(r'^category/(?P<cat>[A-Za-z0-9., ]+)/$', views.category, name='category'),
        url(r'^sendmail/(?P<post>[A-Za-z0-9., ]+)/$', views.send_mail, name='sendmail'),
        url(r'^sendmail/$', views.send_mail, name='sendmail'),
        url(r'^admin_add/$', views.admin_add, name='admin_add'),
        url(r'^admin_delete/(?P<post>[A-Za-z0-9., ]+)/$', views.admin_remove, name='admin_delete'),
        url(r'^give_priv/(?P<un>[A-Za-z0-9., ]+)/$', views.give_priv, name='give_priv'),
        url(r'^userdetails/(?P<un>[A-Za-z0-9., ]+)/$', views.userdetails, name='userdetails'),
        url(r'^admin/$', views.admin, name='admin'),
        
	url(r'^saveData/$', views.saveData, name='saveData'),
	url(r'^sort/(?P<ty>[A-Za-z0-9., ]+)/$', views.sort, name='sort'),
        ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
