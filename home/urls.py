from django.urls import path
from . import views

app_name="home"
urlpatterns = [
    path('', views.shorten_url_form, name="urlForm"),
    path('cp/', views.shorten_code_form, name="codePaste"),

    path('short-urls/', views.display_all_urls, name="urlsDisplay"),
    path('short-code-urls/', views.display_all_codes, name="codesDisplay"),

    path('signup/', views.signup, name="signup"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('home/', views.landingpage, name="landingpage"),

    path('<str:key>/', views.redirect_to_url, name="redirectUrl"),
    path('code/<str:key>/', views.display_code, name="displayCode"),

]
