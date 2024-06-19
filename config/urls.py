from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('myapp/',include('myapp.urls')),
    path('', include('myapp.urls')),

]


#path関数はURLパターンを定義するために使用され、include関数は他のURL設定を含めるために使用


#パスの指定　上から
#管理者画面
#/myapp/というURLにアクセスした場合、myappアプリケーション内のurls.pyファイルで定義されたURLパターンを使用する
#URLが指定されなかった場合も、myapp内のurls.pyのURLパターンを使用する