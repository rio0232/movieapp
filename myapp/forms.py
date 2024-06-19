from django.forms import ModelForm
from myapp.models import Movie, Director, Log
from django import forms
from django.contrib.auth.models import User
from .models import Account

class DateInput(forms.DateInput):
    input_type = 'date'

class DirectorForm(ModelForm):
    class Meta:
        model = Director
        fields = ('name',)

class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ('title','watch_date', 'director')
        widgets = {'watch_date': DateInput(),  # カレンダーウィジェットの指定
    }

class LogForm(ModelForm):
    class Meta:
        model = Log
        fields = ('movie','text')


class AccountForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")
    class Meta:
        model = User
        fields = ('username','email','password')
        labels = {'username':"ユーザーID",'email':"メール"}

