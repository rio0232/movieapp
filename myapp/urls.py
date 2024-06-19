from django.urls import path, include
from . import views


app_name = 'myapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('register/director/', views.RegisterDirectorView.as_view(), name = 'registerdirector'),
    path('register/movie/', views.RegisterMovieView.as_view(), name= 'registermovie'),
    path('writing/log/', views.WritingLogView.as_view(), name = 'writinglog'),
    path('writing/log/<int:pk>/', views.writingthismovielog, name='writing_log'),
    path('update/log/<int:pk>/', views.UpdateLogView.as_view(), name='updatelog'), 
    path('delete/log/<int:pk>/', views.DeleteLogView.as_view(), name='deletelog'), 
    path('delete/movie/<int:pk>/', views.DeleteMovieView.as_view(), name='deletemovie'),
    path('writingthismovielog/<int:pk>/', views.writingthismovielog, name='writingthismovielog'),
    path('register2/', views.AccountRegistration.as_view(), name='register2'),
    path('login/',views.Login,name='Login'),
    path('logout/',views.Logout,name="Logout"),
    path('home/',views.home,name="home"),


]


#urlパターン　上から
#空のパス ('') にマッチする場合、views.IndexViewを呼び出し。name='index'は、このURLパターンに名前を付ける
#<int:pk>は、整数値を受け取るパラメーターで、pkという名前でビューに渡される。この行は、映画の詳細ページを処理。