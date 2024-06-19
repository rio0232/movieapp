from django.db import models
from django.utils import timezone
#Djangoのデフォルトの認証システム
from django.contrib.auth.models import User

#監督名を入れるクラス。nameが監督名
#models.CharFieldは Djangoのモデルフィールドの1つで、文字列データを格納するためのフィールドタイプ
#verbose_nameはデフォルトのフィールド名を上書きし、人間が読みやすい名前にする.

class Director(models.Model):
    name = models.CharField(max_length=100, verbose_name="監督")
    def __str__(self):
        return self.name

#models.DateField(): Djangoのモデルフィールドの1つで、日付を格納するためのフィールドタイプ
#models.ForeignKeyは他のモデルとの関係を表すフィールドタイプ。
#on_delete=models.CASCADEでDirectorが削除されたときにそれに関連するMovieも削除される
#related_nameでDirectorモデルからMovieモデルにアクセスする際の名前を指定

class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name="タイトル")
    director = models.ForeignKey(Director, on_delete=models.CASCADE, verbose_name="監督", related_name='movie')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー", related_name='movies')
    watch_date = models.DateField(verbose_name="視聴日時", null=True, blank=True)

    def __str__(self):
        return self.title

class Log(models.Model):
    text = models.TextField()
    watch_date = models.DateField(default=timezone.now)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="タイトル", related_name='log')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー", related_name='logs')
    

    def __str__(self):
        return self.text


#models.OneToOneFieldは他のモデルとの1対1の関係を表すフィールドタイプ。Userモデルとの関係を定義している。
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
