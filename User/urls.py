from django.conf.urls import url
from User import views
from django.contrib import admin
from .views import (
    PostLikeAPIToggle,

    )


app_name = 'User'

urlpatterns=[
        url(r'^home/$',views.userhome,name='home'),
        url(r'^mapdetails/$',views.Mapdetails,name='mapdetails'),
        url(r'^mapdetailupdate/$',views.Mapdetailupdate,name='mapdetailupdate'),
        url(r'^(?P<slug>[\w-]+)likesupdate/$',views.Likesupdate,name='likesupdate'),
        url(r'^rating/$',views.Rating,name='rating'), 
        url(r'^purchasehistory/$',views.Purchasehistory,name='history'),
        url(r'^(?P<slug>[\w-]+)details/$',views.showitem,name='details'),
        url(r'^(?P<slug>[\w-]+)delete/$',views.deleteitem,name='delete'),
        url(r'^auctions/$',views.auctions,name='auctions'),
        url(r'^deleteauction/$',views.Deleteauction,name='deleteauction'),
        url(r'^(?P<slug>[\w-]+)bid/$',views.bid,name='bid'),
        # url(r'^bids/$',views.bids,name='bids'),
        url(r'^check/$',views.check,name='check'),
        url(r'^deleteitem/$',views.deleteitem,name='deleteitem'),
        url(r'^(?P<type>[\w-]+)allitems/$',views.allitems, name='allitems'),
        url(r'^api/(?P<slug>[\w-]+)/likes/$',PostLikeAPIToggle.as_view(),name='likes-api-toggle'),
        url(r'^(?P<username>[\w-]+)_profile/$',views.userprofile,name='profile'),
        url(r'^sellitem/$',views.sellitem,name='sellitem'),
        url(r'^post/$', views.Post, name='post'),
        url(r'^comment/$', views.Comment, name='comment'),
        url(r'^notification/$', views.Notifications, name='notification'),
        url(r'^messages/(?P<slug>[\w-]+)/$', views.Messages, name='messages'),
        url(r'^filteritem/(?P<string>[\w\-]+)/$', views.Filteritem,name='filteritem'),

]
