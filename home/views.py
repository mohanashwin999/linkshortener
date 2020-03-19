from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from home.models import url_shortener,code_shortener

front_url='https://slcp.herokuapp.com/'

def signup(request):
    '''This function creates an account'''
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        if User.objects.filter(username=username).exists():
            return render(request, "home/signup.html", {'username_error': "Username already exists!"})

        if User.objects.filter(email=email).exists():
            return render(request, "home/signup.html", {'email_error': "Account with entered Email already exists!"})
        
        User.objects.create_user(username=username, email=email, password=password, first_name=fname, last_name=lname)
        return redirect('home:login')
    else:
        return render(request, 'home/signup.html')

def login_user(request):
    '''This function performs login of user'''
    if(request.user.is_authenticated):                      #already logged in
        return redirect('home:dashboard')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:            
            login(request, user)
            return redirect('home:dashboard')
        else:
            messages.error(request,'Invalid Username or Password')
            return render(request, 'home/login.html')
    else:
        return render(request, 'home/login.html')


def landingpage(request):
    '''landing page if user isnt logged in'''
    return render(request,'home/landingpage.html')

@login_required
def logout_user(request):
    '''This function logouts the user'''
    logout(request)
    return redirect('home:login')

@login_required
def dashboard(request):
    '''This function displays the landing page'''
    return render(request, 'home/dashboard.html')

def shorten_url_form(request):
    ''' This function receives URL and back-half from post method and add to database '''
    if request.method == "POST":
        username = request.POST.get("username")
        url = request.POST.get("url")
        back_half = request.POST.get("backhalf")
        description = request.POST.get("description")

        if username != '':                                               # check username
            try:                                                   
                User.objects.get(username=username)
            except:
                return render(request, "home/url_form.html", {'username_error': "Entered username does not exist!"})

        sobj = url_shortener.objects.all()                               # check back half already present
        back_half_list = []
        for x in sobj:
            back_half_list.append(x.back_half)
        if back_half in back_half_list:
            return render(request, "home/url_form.html", {'backhalf_error': "Entered Back-Half already exists!"})

        s = url_shortener()                                              # database entry
        s.url = url
        s.back_half = back_half
        s.description = description
        s.username = username
        s.save()

        return_url = front_url+back_half+'/'
        return render(request, "home/url_form.html", {'url': return_url})
    else:
        return render(request, "home/url_form.html")


def redirect_to_url(request, key):
    '''This function receives back-half as parameter and redirects to URL stored in database'''
    try:
        sobj = url_shortener.objects.get(back_half=key)         #select url from back-half
        url = sobj.url
        return redirect(url)
    except:
        return HttpResponse("<h1>ShortLink says:</h1><p>No such URL found</p>",content_type="html")


def shorten_code_form(request):
    ''' This function receives code and back-half from post method and add to database '''
    if request.method == "POST":
        username = request.POST.get("username")
        code = request.POST.get("code")
        back_half = request.POST.get("backhalf")
        description = request.POST.get("description")

        if username != '':                                               # check username
            try:                                                   
                User.objects.get(username=username)
            except:
                return render(request, "home/code_form.html", {'username_error': "Entered username does not exist!"})

        c = code_shortener()                                              # database entry
        c.code = code
        c.back_half = back_half
        c.description = description
        c.username = username
        c.save()

        return_url = front_url+'code/'+back_half+'/'
        return render(request, "home/code_form.html", {'url': return_url})
    else:
        return render(request, "home/code_form.html")

def display_code(request,key):
    '''This function receives back-half as parameter and displays your pasted code'''
    try:
        cobj = code_shortener.objects.get(back_half=key)
        code = cobj.code
        return render(request, "home/display_code.html",{'code':code})
    except:
        return HttpResponse("<h1>ShortLink says:</h1><p>No such URL found</p>",content_type="html")

@login_required
def display_all_codes(request):
    '''Display all short-code-links of the user'''
    codes_list=[]
    cobj=code_shortener.objects.filter(username=request.user)
    for i in cobj:
        codes_list.append([i.description , front_url+'code/'+i.back_half+'/'])
    return render(request, "home/display_codes.html",{'codes':codes_list})

@login_required
def display_all_urls(request):
    '''Display all short-URLs of the user'''
    urls_list=[]
    sobj=url_shortener.objects.filter(username=request.user)
    for i in sobj:
        urls_list.append([i.description, i.url , front_url+i.back_half+'/'])
    return render(request, "home/display_urls.html",{'urls':urls_list})