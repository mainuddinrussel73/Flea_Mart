from django.shortcuts import render,redirect
from firstapp.forms import UserForm,UserProfileInform
from django.shortcuts import render,get_object_or_404
from .models import UserProfileInfo,User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout
from User.models import SellItemInfo
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.db.models import Q
from datetime import datetime

lock = True

def error_404(request):
    return render(request,'firstapp/404.html')

def error_500(request):
    return render(request,'firstapp/404.html')

def index(request):
    items = SellItemInfo.objects.all()
    args = {'items' : items}
    return render(request,'firstapp/index.html', args,)

def forgotPassword(request):
    return render(request,'firstapp/forgotpassword.html')

def Updatepass(request):
    lock = UserProfileInfo.objects.get(user=request.user)
    if lock.istimeout == True:
        UserProfileInfo.objects.filter(user=request.user).update(istimeout=False)
        return render(request,'firstapp/updatepass.html')
    else:
        context = {
            'Notice':'Sorry Time out Occured'

        }
        return render(request,'firstapp/forgotpassword.html',context)

def Set_password(request):
    if request.POST:
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = User.objects.get(username=username)
        if(not user):
            context = {
                'Notice':'Please User Correct Email Address'

            }
            return render(request,'firstapp/updatepass.html',context)
        else:
            # send_mail("Your PW", user.password , "admin@example.com", [email])

            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse('firstapp:login'))
        return render(request,'firstapp/updatepass.html',context)

def resetPassword(request):
    if request.POST:
        email=request.POST.get("email")
        username=request.POST.get("username")
        password=request.POST.get("password")
        # print (email)
        user = User.objects.filter(username=username,email=email)
        us = User.objects.filter(username=username,email=email)


        # print(user)
        if(not user or user.count()==0):
            # print "No user"
            context = {
                'Notice':'Something is not correct'

            }
            return render(request,'firstapp/forgotpassword.html',context)
        else:
            # send_mail("Your PW", user.password , "admin@example.com", [email])
            UserProfileInfo.objects.filter(user=request.user).update(istimeout=True)
            email = EmailMessage('Your PW', "http://127.0.0.1:8000/fleamart/updatepass/" , to=[email])
            email.send()
            return HttpResponseRedirect(reverse('firstapp:login'))
    return render(request,'firstapp/forgotpassword.html')
@login_required
def userlogout(request):
    logout(request)
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == "POST":
        userform = UserForm(data=request.POST)
        profileform = UserProfileInform(data=request.POST)

        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()

            profile = profileform.save(commit=False)
            profile.user = user

            if 'profilepic' in request.FILES:
                profile.profilepic = request.FILES['profilepic']

            profile.save()
            registered = True
            return redirect('/')

        else :
            print('Not possible')
    else:
        userform = UserForm()
        profileform = UserProfileInform()

    return render(request,'firstapp/registration.html',
    {
        'userform':userform,
        'profileform':profileform,
        'registered':registered
    })


def userlogin(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        global userName

        userName = username
        user = authenticate(username=username,password=password)


        if user:
            if user.is_active:
                auth_login( request , user )
                request.session['time_out'] = user.username
                return redirect('/User/home/')
            else:
                return HttpResponse("Account is not active")
        else:
            context = {
                'Notice':'Please User Correct UserName or Password'

            }
            return render(request,'firstapp/login.html',context)
    else:
        return render(request,'firstapp/login.html')






@login_required
def Update(request):
    u = get_object_or_404(User,username=request.user.username)
    a = get_object_or_404(UserProfileInfo,user=request.user)
    userform = UserForm(request.POST or None ,instance=u)
    profileform = UserProfileInform(request.POST or None ,instance=a)
       
    if userform.is_valid() and profileform.is_valid():

        user = userform.save()
        user.set_password(user.password)
        user.save()

        profile = profileform.save(commit=False)
        profile.user = user

        if 'profilepic' in request.FILES:
            profile.profilepic = request.FILES['profilepic']

        profile.save()
        return redirect('/')
    return render(request,'firstapp/update.html',
    {
        'userform' : userform,
        'profileform' : profileform
    })    



def Aboutus(request):

    return render(request,'firstapp/aboutus.html',{})    

def Faq(request):

    return render(request,'firstapp/faq.html',{})    