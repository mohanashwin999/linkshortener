from django.urls import path
from . import views

app_name="home"
urlpatterns = [
    path('link-short/', views.shorten_url_form, name="urlForm"),
    path('code-paste/', views.shorten_code_form, name="codePaste"),
    path('upload-media/', views.media_upload, name="mediaUpload"),

    path('short-urls/', views.display_all_urls, name="urlsDisplay"),
    path('short-code-urls/', views.display_all_codes, name="codesDisplay"),
    path('media-all/', views.display_all_media, name="mediaDisplay"),

    path('signup/', views.signup, name="signup"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('', views.landingpage, name="landingpage"),

    path('link/<str:key>/', views.redirect_to_url, name="redirectUrl"),
    path('code/<str:key>/', views.display_code, name="displayCode"),
    path('file/<str:key>/', views.return_media, name="returnMedia"),

    path('delete-link/<int:id>/', views.delete_link, name="deleteLink"),
    path('delete-code/<int:id>/', views.delete_code, name="deleteCode"),
    path('delete-media/<int:id>/', views.delete_media, name="deleteMedia"),


]

