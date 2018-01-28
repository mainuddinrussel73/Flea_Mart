from django.shortcuts import render,get_object_or_404
from firstapp.forms import UserForm,UserProfileInform
import json
from firstapp.models import UserProfileInfo,User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login as auth_login,logout
from User.forms import SellItemInfoForm,CommentsForm,AuctionsForm
from User.models import SellItemInfo,Chat,Notification,Comments,ServerInfo,Auctions,purchaseInfo,RatingInfo
from django.core import serializers
from django.forms.models import model_to_dict
from itertools import chain,cycle
try:
    from itertools import zip_longest as zip_longest
except:
    from itertools import izip_longest as zip_longest
import re
from collections import Counter
import string
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import RedirectView
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, datetime
import json
import decimal
import ast
import locale
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.db.models import Count
from django.db.models.query import QuerySet
# from django.core import serializers
# json_serializer = serializers.get_serializer("json")()
# companies = json_serializer.serialize(Notification.objects.all().order_by('id')[:5], ensure_ascii=False)

# Create your views here.

other = None
nam = ""
iteuploader = None
slugg_ = None
teruser = None



def Rating(request):
    if request.method == "POST":
        rating = request.POST['dat']
        slug = request.POST['slug']
        print(rating)
        print(slug)
        ii = SellItemInfo.objects.get(slug=slug)
        r = RatingInfo.objects.filter(user=request.user,item=ii)
        u = RatingInfo.objects.all()
        k = RatingInfo.objects.filter(item=ii).values('rate').annotate(total=Count('rate')).order_by('-rate')
        
        hh = list(k.values('rate','total'))
        ll = []
        rr = []
        c = 0
        for i in hh:
            rr.insert(c,i.get('rate'))
            ll.insert(c,i.get('total'))
            c+=1

        # print(rr)
        # print(ll)
        if r.count()==0:
            rr = RatingInfo(user=request.user,item=ii,rate=rating)
            rr.save()
            k = RatingInfo.objects.filter(item=ii).values('rate').annotate(total=Count('rate')).order_by('-rate')
        
            hh = list(k.values('rate','total'))
            ll = []
            rr = []
            c = 0
            for i in hh:
                rr.insert(c,i.get('rate'))
                ll.insert(c,i.get('total'))
                c+=1
            return JsonResponse({ 'msg': "Thank You For Rating This Item" ,"d":"done","rr":ll,"lab":rr, "hh":hh })
        else:
            rr = RatingInfo.objects.filter(user=request.user,item=ii).update(rate = rating)
            
            k = RatingInfo.objects.filter(item=ii).values('rate').annotate(total=Count('rate')).order_by('-rate')
        
            hh = list(k.values('rate','total'))
            ll = []
            rr = []
            c = 0
            for i in hh:
                rr.insert(c,i.get('rate'))
                ll.insert(c,i.get('total'))
                c+=1
            return JsonResponse({ 'msg': "Thank You For Rating  again" ,"d":"done","rr":ll,"lab":rr, "hh":hh})
    # return HttpResponse(rating)
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def json_encode_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")

@login_required
def Mapdetailupdate(request):
    items = SellItemInfo.objects.all().exclude(uploader=request.user)
    hhh = list(items.values('uploader','item_name','item_lat','item_long','item_location','slug'))
    return HttpResponse(json.dumps(hhh,default=json_encode_decimal))

@login_required
def Mapdetails(request):
    return render(request,'firstapp/locations.html',{},)

@login_required
def bid(request,slug=None):
    form = AuctionsForm(request.POST or None)
    if request.method == 'POST':
        form = AuctionsForm(data=request.POST)
        bids = request.POST.get('bids', None)
        # print(bids)
        ii = SellItemInfo.objects.get(slug=slug)
        auctions_pre = Auctions.objects.filter(item=ii)
        ggg = list(auctions_pre.values('bids'))
        s = ggg[0].get('bids')
        if(s<int(bids)):
            auctions = Auctions.objects.filter(item=ii).update(bids = bids,biders=request.user.username)
        return HttpResponseRedirect(reverse('User:auctions'))
    else:
        item = SellItemInfo.objects.get(slug=slug);
        auct = Auctions.objects.filter(item=item);
        ggg = list(auct.values('duration'))
        return render(request, 'firstapp/auction_details.html', { "AuctionsForm":form,"item" : item ,"auct":json.dumps(ggg,default=json_serial)})



@login_required
def check(request):

    if request.method == "POST":
        status = request.POST.get('status', None)
        dateTime = request.POST.get('time', None)
        slug =   request.POST.get('slug', None)
        # print(dateTime)
        # print(status)
        # print(slug)
        it = SellItemInfo.objects.filter(slug=slug).update(isAuction=True)
        itr = SellItemInfo.objects.get(slug=slug)
        # print(itr)
        o =  Auctions.objects.filter(item=itr)
        # print(o)
        if o.count()==0:
            obj = Auctions(uploader=request.user,item=itr,bids=0,biders=request.user.username,isAuction=True,duration=dateTime)
            obj.save()
        # ggg = list(obj.values('isAuction'))
        # print(ggg)
    return HttpResponse(slug)

@login_required
def auctions(request):
    obj = Auctions.objects.filter(isAuction=True).exclude(uploader=request.user)
    # print(obj)
    # print(obj.count())
    args = {
        "items" : obj,
        "count" : obj.count()
    }
    return render(request, 'firstapp/auction.html', args,)

@login_required
def Deleteauction(request):
    if request.method == "POST":
        slug = request.POST.get('slug', None)
        itr = SellItemInfo.objects.get(slug=slug)

        obj = Auctions.objects.filter(item=itr).exclude(uploader=request.user)
        o = Auctions.objects.get(item=itr)
        # print(o)
        us = User.objects.get(username=o.biders)
        if(obj.count()>0):
            obj.delete()
        n = Notification(user=us,to=o.uploader.username,fromm=o.biders,count=slug,description="selected")
        m = Notification.objects.filter(user=us,count=slug,to=o.uploader.username)
        if m.count()==0 :
            n.save()
        return HttpResponseRedirect(reverse('User:auctions'))


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(SellItemInfo, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        ne = 0
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
                obj.likecount-=1
                ne = obj.likecount
                obj.save()
            else:
                liked = True
                obj.likes.add(user)
                obj.likecount+=1
                ne = obj.likecount
                obj.save()
            updated = True
        data = {
            "updated": updated,
            "liked": liked,
            "ne"   :  ne
        }
        return Response(data)

@login_required
def Purchasehistory(request):
    p = purchaseInfo.objects.filter(user=request.user).order_by("-timestemp")
    args = {
        "p" : p
    }
    return render(request, 'firstapp/purchasehistory.html', args,)


@login_required
def deleteitem(request):
    if request.method == "POST":
        name = request.POST.get('name', None)
        price = request.POST.get('price', None)
        slug = request.POST.get('slug', None)
        obj = SellItemInfo.objects.filter(slug=slug)
        obb = SellItemInfo.objects.get(slug=slug)

        p = purchaseInfo(user=request.user,itemname=slug,item_pic=obb.item_pic,buyer=name,price=price)
        p.save()
        if(obj.count()>0):

            obj.delete()

        obj1 = SellItemInfo.objects.filter(uploader=request.user)
        args = {
            "items" : obj1
        }
        return render(request, 'firstapp/profile.html', args,)

@login_required
def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        global other
        global iteuploader
        global teruser
        other = request.POST.get('hide', None)
        itemname = request.POST.get('itemname', None)
        iteuploader = request.POST.get('iteuploader', None)
        teruser = request.POST.get('docc',None)
        slug = request.POST.get('my',None)
        print(slug)
        # print(teruser)
        u = User.objects.get(username=iteuploader)

        print(u)
        if iteuploader == request.user.username:
            try:
                it = SellItemInfo.objects.get(uploader=u,slug=slug)
                print(it)
            except:
                pass
            c = Chat(user=request.user,item=it, message=msg,fromm=teruser,to=request.user.username)
        else:
            try:
                it = SellItemInfo.objects.get(uploader=u,slug=slug)
                print(it)
            except:
                pass
            c = Chat(user=request.user,item=it, message=msg,fromm=iteuploader,to=request.user.username)
        counter = SellItemInfo.objects.get(item_name=itemname)
        n = Notification(user=request.user,to=request.user.username,fromm=iteuploader,count=counter.get_slug(),description=msg)
        if iteuploader == request.user.username:
            m = Notification.objects.filter(user=request.user,count=counter.get_slug(),fromm=teruser)
            if msg != ' ':
                c.save()
            if m.count()==0 and request.user.username != iteuploader:
                n.save()
            elif  m.count()==0 and  request.user.username == iteuploader:
                nn = Notification(user=request.user,to=request.user.username,fromm=teruser,count=counter.get_slug(),description=msg)
                nn.save()
        else :
            m = Notification.objects.filter(user=request.user,count=counter.get_slug(),to=request.user.username)
            if msg != '':
                c.save()
            if m.count()==0 and request.user.username != iteuploader:
                n.save()
            elif  m.count()==0 and  request.user.username == iteuploader:
                nn = Notification(user=request.user,to=request.user.username,fromm=teruser,count=counter.get_slug(),description=msg)
                nn.save()

        return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')

@login_required
def Messages(request,slug):

    print(slug)
    it = SellItemInfo.objects.get(slug=slug)
    print(it)
    c = Chat.objects.filter(item=it)
    # print(c)

    use = User.objects.exclude(username=request.user.username)
    # print(counter)
    hhh = list(use.values('username'))
    # print(json.dumps(hhh))
    # print(c)
    # print(request.user.username)
    # print(iteuploader)
    # print(teruser)
    return render(request, 'firstapp/messages.html', {'chat': c,'other':teruser,'iteuploader':iteuploader,'use':json.dumps(hhh) })




@login_required
def Likesupdate(request,slug=None):

    if request.is_ajax():
        obj = SellItemInfo.objects.filter(slug=slug)

        obj_ = []

        obj_ = list(obj.values('likecount'))
        # print(json.dumps(obj_))
        return HttpResponse(json.dumps(obj_))


@login_required
def Notifications(request,username='main'):

    if request.is_ajax():
        counter = Notification.objects.filter(fromm=request.user.username)
        # print(counter)
        hhh = list(counter.values('to','fromm','description','count','id'))
        index = 0
        lll = []
        for u in hhh:
            ss = User.objects.get(username=u.get('to'))
            bonus = UserProfileInfo.objects.filter(user=ss)
            # print(bonus)
            ggg = list(bonus.values('user','profilepic','user_id'))

            for o in ggg:
                # print(o.get('profilepic'))
                nnn = {
                    'id' : o.get('user'),
                    'profilepic' : o.get('profilepic'),
                    'to' : u.get('to'),
                    'description' : u.get('description'),
                    'count' : u.get('count'),
                    'fromm' : u.get('fromm')
                }
                lll.insert(index,nnn)
                index+=1
        # print(request.session['username'])
        try:
            del request.session['username']
            logout(request)
            return HttpResponseRedirect(reverse('index'))
        except KeyError:
            pass
        # print(request.session['username'])
        

        # print(json.dumps(lll))

        return HttpResponse(json.dumps(lll))
def compare(s1, s2):
    remove = string.punctuation + string.whitespace
    return s1.translate(None, remove) == s2.translate(None, remove)
def combine(list1, list2):
    list1 = iter(list1)
    for item2 in list2:
        if item2 == list2[0]:
            item1 = next(list1)
        yield ''.join(map(str, (item1, item2)))



def allitems(request,type=None):
    # print(type)
    it = SellItemInfo.objects.values('item_type').distinct()
    items_list = SellItemInfo.objects.all().order_by("-timestemp")
    items_list = items_list.filter(
                Q(slug__icontains=type) |
                Q(item_name__icontains=type) |
                Q(item_location__icontains=type)|
                Q(item_type__icontains=type)
                ).distinct()
    paginator = Paginator(items_list,6)
    page_request_var = 'page'

    page = request.GET.get(page_request_var)
    try :
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except:
        items = paginator.page(paginator.num_pages)
    args = {'items' : items,"page_request_var" : page_request_var,"it":it }
    return render(request,'firstapp/itemwithoulogin.html',args)


def Filter(request,keywrd):
    u = User.objects.get(username=request.user.username)
    counter = Notification.objects.filter(fromm=request.user.username)


    if keywrd != 'showall':
        items_list = SellItemInfo.objects.filter(item_type=keywrd).order_by("-timestemp")
    else:
        keywrd = 'All'
        items_list = SellItemInfo.objects.all().order_by("-timestemp")

    it = SellItemInfo.objects.values('item_type').distinct()
    queary = request.GET.get("q")
    if queary :
        items_list = items_list.filter(
            Q(slug__icontains=queary) |
            Q(item_name__icontains=queary) |
            Q(item_location__icontains=queary)|
            Q(item_type__icontains=queary)
        ).distinct()

    paginator = Paginator(items_list,6)
    page_request_var = 'page'

    page = request.GET.get(page_request_var)
    try :
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except:
        items = paginator.page(paginator.num_pages)

    # print(items_list)
    args = {'items' : items,'counter' : counter ,"c" : counter.count(),"page_request_var" : page_request_var,"it":it ,"key":keywrd}
    return args






@login_required
def Filteritem(request,string):
    
           
            print(string)
            print("posted")
            args = Filter(request,string)
            return render(request,'firstapp/userhome.html',args)


@login_required
def userhome(request,username=None):
    print(request.POST)
    if 'showall' in request.POST :
        args = Filter(request,'showall')
        return render(request,'firstapp/userhome.html',args)
    elif 'phone' in request.POST:
        args = Filter(request,'phone')
        return render(request,'firstapp/userhome.html',args)
    elif 'guiter' in request.POST:
        args = Filter(request,'guiter')
        return render(request,'firstapp/userhome.html',args)
    elif 'laptop' in request.POST:
        args = Filter(request,'laptop')
        return render(request,'firstapp/userhome.html',args)
    elif 'tablet' in request.POST:
        args = Filter(request,'tablet')
        return render(request,'firstapp/userhome.html',args)
    elif 'camera' in request.POST:
        args = Filter(request,'camera')
        return render(request,'firstapp/userhome.html',args)
    elif 'console'in request.POST:
        args = Filter(request,'console')
        return render(request,'firstapp/userhome.html',args)
    elif 'range' in request.POST:
        # print(request.POST['range'])
        a = request.POST['range']
        u = User.objects.get(username=request.user.username)
        counter = Notification.objects.filter(fromm=request.user.username)
        items_list = SellItemInfo.objects.filter(item_exprice__lte=a).order_by("-timestemp")
        it = SellItemInfo.objects.values('item_type').distinct()
        queary = request.GET.get("q")
        if queary :
            items_list = items_list.filter(
                    Q(slug__icontains=queary) |
                    Q(item_name__icontains=queary) |
                    Q(item_location__icontains=queary)|
                    Q(item_type__icontains=queary)
                    ).distinct()

        paginator = Paginator(items_list,6)
        page_request_var = 'page'

        page = request.GET.get(page_request_var)
        try :
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except:
            items = paginator.page(paginator.num_pages)

        # print(items_list)
        args = {'items' : items,'counter' : counter ,"c" : counter.count(),"page_request_var" : page_request_var,"it":it,"key":"All" }
        return render(request,'firstapp/userhome.html',args)
    else:
        u = User.objects.get(username=request.user.username)

        counter = Notification.objects.filter(fromm=request.user.username)


        items_list = SellItemInfo.objects.all().order_by("-timestemp")
        it = SellItemInfo.objects.values('item_type').distinct()
        queary = request.GET.get("q")
        if queary :
            items_list = items_list.filter(
                    Q(slug__icontains=queary) |
                    Q(item_name__icontains=queary) |
                    Q(item_location__icontains=queary)|
                    Q(item_type__icontains=queary)
                    ).distinct()

        paginator = Paginator(items_list,6)
        page_request_var = 'page'

        page = request.GET.get(page_request_var)
        try :
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except:
            items = paginator.page(paginator.num_pages)

        # print(items_list)
        args = {'items' : items,'counter' : counter ,"c" : counter.count(),"page_request_var" : page_request_var,"it":it,"key":"All" }
        return render(request,'firstapp/userhome.html',args)

@login_required
def userprofile(request,username=None,pk=None):
    i = ServerInfo.objects.all()
    # print(list(i.values('videos')))
    if pk:
        user = User.objects.get(pk=pk)
        username = user.username


    else:
        user = request.user
        username = user.username

    items = SellItemInfo.objects.filter(uploader=user)
    args = {'user': user,'items' : items,'i':i}
    return render(request, 'firstapp/profile.html', args,)



@login_required
def Comment(request):


    if request.method == 'POST':
        co = request.POST['co']
        slug = request.POST['slug']

        # print(slug)
        # print(co)
        item = SellItemInfo.objects.get(slug=slug);
        username = request.user.username
        c = Comments(user=request.user,item=item,username=request.user.username,content=co)

        if co != '':
             c.save()

        return JsonResponse({ 'comm': co, 'user': request.user.username,'timestemp':c.timestemp,'profilepic' : request.user.userprofileinfo.profilepic.url })
    else:
        return HttpResponse('Request must be POST.')
@login_required
def showitem(request,slug=None,id=None):


    instance = get_object_or_404(SellItemInfo,slug=slug);
    # instance = SellItemInfo.objects.get(item_name=item_name)
    comments = Comments.objects.filter(item=instance);


    c = Chat.objects.filter(user=request.user)
    if iteuploader == request.user.username:
        v = Chat.objects.all()
    else:
        v = Chat.objects.filter(fromm=teruser)
    # u = request.get('id')
    global nam
    namw = ""
    global slug_
    slug_ = slug
    obj = get_object_or_404(SellItemInfo, slug=slug)
    user = request.user
    liked = False
    if user.is_authenticated():
        if user in obj.likes.all():
            liked = "Unlike"
        else:
            liked = "Like"

    if slug!=None:
        try:
            ins = Notification.objects.get(count=slug,fromm=request.user.username)
            # print(ins)
            i = Notification.objects.get(count=slug,fromm=request.user.username)
            namw = i.to

            ins.delete()

        except ObjectDoesNotExist:
            ins = None
            i = None
            namw = ""


        # print(ins)


    # r      =     RatingInfo.objects.filter(item=instance)
    r = RatingInfo.objects.filter(item=instance).values('rate').annotate(total=Count('rate')).order_by('-rate')
    print(r)
    use = User.objects.exclude(username=request.user.username)
    # print(counter)
    hhh = list(use.values('username'))
    al = SellItemInfo.objects.all().exclude(slug=slug).exclude(uploader=request.user)
    print(al)
    # print(json.dumps(hhh))
    # for r in instance:
        # r.delete()
    nam = namw

    args = {
        "instance" : instance,
        'chat': c,
        'nam' : nam,
        "liked": liked,
        "obj" : obj,
        "comments" : comments,
        "v"    : v,
        "use" : json.dumps(hhh),
        "r" : r,
        "al" : al,

     }
    return render(request, 'firstapp/details.html', args,)

@login_required
def sellitem(request):

    isposted = False

    if request.method == "POST":
        # userform = UserForm(data=request.POST)
        selliteminfo = SellItemInfoForm(data=request.POST)

        if selliteminfo.is_valid():
            # user = userform.save()
            # user.set_password(user.password)
            # user.save()

            item = selliteminfo.save(commit=False)
            item.uploader = request.user
            item.save()
            # profile.user = user

            if 'item_pic' in request.FILES:
                item.item_pic = request.FILES['item_pic']

            item.save()
            isposted = True


    else:
        # userform = UserForm()
        selliteminfo = SellItemInfoForm()  #sett item forms

    return render(request,'firstapp/sellitem.html',
    {

        'selliteminfo':selliteminfo,
        'isposted':isposted
    })
