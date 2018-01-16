from django.conf.urls import url
from firstapp import views


app_name = 'firstapp'

urlpatterns=[



        url(r'^register/$',views.register,name='register'),
        url(r'^update/$',views.Update,name='update'),
        url(r'^login/$',views.userlogin,name='login'),
        url(r'^error_404/$',views.error_404,name='error_404'),
        url(r'^error_500/$',views.error_500,name='error_500'),
        url(r'^forgetemail/$',views.forgotPassword,name='forgetemail'),
        url(r'^resetpass/$',views.resetPassword,name='resetpass'),
        url(r'^updatepass/$',views.Updatepass,name='updatepass'),
        url(r'^set_password/$',views.Set_password,name='set_password'),
        url(r'^aboutus/$',views.Aboutus,name='aboutus'),
        url(r'^faq/$',views.Faq,name='faq'),



]
