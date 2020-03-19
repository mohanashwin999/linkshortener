from django.contrib import admin
from .models import code_shortener,url_shortener

admin.site.register([code_shortener,url_shortener])
