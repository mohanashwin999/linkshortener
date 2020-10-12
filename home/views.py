from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from home.models import url_shortener, code_shortener, media_uploader
from urlshortener.config import BUCKET_URL


#front_url = 'https://slcp.herokuapp.com/'
bucket_url = BUCKET_URL
front_url = 'http://localhost:8000/'  #for development

def signup(request):
    '''This function creates an account'''
    
    if request.method == 'POST':                                            #post method
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
   
    else:                                                              #get method
        return render(request, 'home/signup.html')


def login_user(request):
    '''This function performs login of user'''
    
    if(request.user.is_authenticated):                                          # already logged in
        return redirect('home:dashboard')

    if request.method == "POST":                                                #post method
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)                                        #add all user details to request for session 
            return redirect('home:dashboard')
        else:
            messages.error(request, 'Invalid Username or Password')
            return render(request, 'home/login.html')
   
    else:                                               #get method
        return render(request, 'home/login.html')


def landingpage(request):
    '''landing page if user isnt logged in'''
    
    return render(request, 'home/landingpage.html')             # get display page


@login_required
def logout_user(request):
    '''This function logouts the user'''
    
    logout(request)                                                     #remove user details from request
    return redirect('home:login')


@login_required
def dashboard(request):
    '''This function displays the landing page'''
    
    return render(request, 'home/dashboard.html')


def shorten_url_form(request):
    ''' This function receives URL and back-half from post method and add to database '''
   
    if request.method == "POST":                                            #post method
        username = request.POST.get("username") 
        url = request.POST.get("url")
        back_half = request.POST.get("backhalf")
        description = request.POST.get("description")

        if username != '' and not User.objects.filter(username=username).exists():         #if username is entered and username does not exist      
            return render(request, "home/url_form.html", {'username_error': "Entered username does not exist! Please Signup."})

        if url_shortener.objects.filter(back_half=back_half).exists():                  # check back half exist 
            return render(request, "home/url_form.html", {'backhalf_error': "Entered Back-Half already exists!"})
        else:
            s = url_shortener()
            s.url = url
            s.back_half = back_half
            s.description = description
            s.username = username
            s.save()

        return_url = front_url+ 'link/' + back_half+'/'
        return render(request, "home/url_form.html", {'url': return_url})
    
    else:                                                                             #get method
        return render(request, "home/url_form.html")


def redirect_to_url(request, key):
    '''This function receives back-half as parameter and redirects to URL stored in database'''
   
    try:
        sobj = url_shortener.objects.get(back_half=key)                  # select url from back-half
        return redirect(sobj.url)
    
    except:
        return render(request, "home/error.html")


def shorten_code_form(request):
    ''' This function receives code and back-half from post method and add to database '''
   
    if request.method == "POST":                                    #post method
        username = request.POST.get("username")
        code = request.POST.get("code")
        back_half = request.POST.get("backhalf")
        description = request.POST.get("description")

        if username != '' and not User.objects.filter(username=username).exists():         #if username is entered and username does not exist      
            return render(request, "home/code_form.html", {'username_error': "Entered username does not exist! Please Signup."})
       
        if code_shortener.objects.filter(back_half=back_half).exists():                 #back-half exists check
            return render(request, "home/code_form.html", {'backhalf_error': "Entered Back-Half already exists!"})
        else:
           
            c = code_shortener()                                                     # database entry
            c.code = code
            c.back_half = back_half
            c.description = description
            c.username = username
            c.save()

        return_url = front_url+'code/'+back_half+'/'
        return render(request, "home/code_form.html", {'url': return_url})
   
    else:                                                                    #Get method
        return render(request, "home/code_form.html")

def media_upload(request):
    if request.method == "POST":                                    #post method
        file = request.FILES["file"]
        username = request.POST.get("username")
        back_half = request.POST.get("backhalf")
        description = request.POST.get("description")

        if not username:
            return render(request, "home/media_form.html", {'username_error': "Username is required for uploading media!"})

        if file.size > 3145728:
            return render(request, "home/media_form.html", {'size_error': "File size greater than 3MB!"})
        

        if username != '' and not User.objects.filter(username=username).exists():         #if username is entered and username does not exist      
            return render(request, "home/media_form.html", {'username_error': "Entered username does not exist! Please Signup."})
       
        if media_uploader.objects.filter(back_half=back_half).exists():                 #back-half exists check
            return render(request, "home/media_form.html", {'backhalf_error': "Entered Back-Half already exists!"})
        else:
           
            m = media_uploader()                                                     # database entry
            m.file = file
            m.back_half = back_half
            m.description = description
            m.username = username
            m.save()

        return_url = front_url+'file/'+back_half+'/'
        return render(request, "home/media_form.html", {'url': return_url})
   
    else:                                                                    #Get method
        return render(request, "home/media_form.html")

   
def return_media(request, key):
    try:
        mobj = media_uploader.objects.get(back_half = key)
        url = bucket_url + str(mobj.file)
        return redirect(url)
    except:
        return render(request, "home/error.html")

def display_code(request, key):
    '''This function receives back-half as parameter and displays your pasted code'''
   
    try:
        cobj = code_shortener.objects.get(back_half=key)
        return render(request, "home/display_code.html", {'code': cobj.code})
    except:
        return render(request, "home/error.html")


@login_required
def display_all_codes(request):
    '''Display all short-code-links of the user logged in'''
   
    cobj = code_shortener.objects.filter(username=request.user).order_by('-date_time')                  #filter by username descending order
    return render(request, "home/display_codes.html", {'codes': cobj, 'url' : front_url+'code/'})


@login_required
def display_all_urls(request):
    '''Display all short-URLs of the user logged in'''
   
    uobj = url_shortener.objects.filter(username=request.user).order_by('-date_time')                    #filter by username descending order
    return render(request, "home/display_urls.html", {'urls': uobj, 'url' : front_url})

@login_required
def display_all_media(request):
    '''Display all files of the user logged in'''
   
    cobj = media_uploader.objects.filter(username=request.user).order_by('-date_time')                  #filter by username descending order
    return render(request, "home/display_media.html", {'media': cobj, 'url' : front_url+'file/'})


@login_required
def delete_code(request, id):
    try:
        code_shortener.objects.get(pk=id).delete()
    except:
        pass
    return redirect('home:codesDisplay')  

@login_required     
def delete_link(request, id):
    try:
        url_shortener.objects.get(pk=id).delete()
    except:
        pass
    return redirect('home:urlsDisplay')

@login_required     
def delete_media(request, id):
    try:
        media_uploader.objects.get(pk=id).delete()
    except:
        pass
    return redirect('home:mediaDisplay')


