from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    
	url(r'^$', 'app.views.home',name='homeurl'),
    url(r'^signup/$','app.views.signup',name='signupurl'),
    url(r'^verifylogin/$','app.views.loginverify',name='verifyloginurl'),
    url(r'^verifysignup/$','app.views.signupverify',name='verifysignupurl'),
    url(r'^login/$','app.views.login',name='loginurl'),
   # url(r'^imgurl/$','app.views.imageviewer',name='imgurl'),
    url(r'^uploadpic/$','app.views.uploadpic',name='uploadpic'),
	)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
