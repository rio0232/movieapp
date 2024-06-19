from django.contrib import admin
from myapp.models import Director, Movie, Log
from .models import Account

admin.site.register(Account)

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Log)


