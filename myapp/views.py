from django.views import generic
from myapp.models import Movie, Director, Log 
from django.shortcuts import render
from django.urls import reverse
from myapp.forms import DirectorForm, MovieForm, LogForm
from django.shortcuts import get_object_or_404, redirect
from .models import Movie
from django.views.generic import ListView
from django.views.generic import TemplateView 
from .forms import AccountForm
from django.http import HttpResponseBadRequest

# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


#generic.ListViewを継承。これはDjangoが提供する汎用のリストビュー
#template_name =ビューがレンダリングするテンプレートのファイルパスを指定
#context_object_nameテンプレートに渡されるコンテキスト変数の名前を指定。の変数名は、テンプレート内で映画リストにアクセスするために使用。
#get_querysetメソッドは、クエリセット(DBから指定した条件で検索した結果)を返す
#queryはユーザーが検索フォームに入力したキーワード
#icontainsは部分一致で、大文字と小文字を区別せずに検索する

class IndexView(generic.ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'movie_list'
    
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            movie_list = Movie.objects.filter(title__icontains=query)
        else:
            movie_list = Movie.objects.all()
        return movie_list

#DetailViewは、特定のオブジェクトの詳細ページを表示するための汎用ビュー

class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'myapp/detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Movieモデルから関連するLogモデルを取得してcontextに追加
        context['logs'] = self.object.log.all()
        return context


#新しい監督を登録するためのビュー
#CreateViewは、新しいオブジェクトを作成するための汎用ビュー
#form_class = このクラスで使用するフォームを指定。フォームクラスはforms.pyで定義
#def get_success_url(self):オブジェクトの作成が成功した後にリダイレクトする先のURLを返すメソッドを定義
#reverse(URLパターンの名前を表す文字列(urls.pyで定義したやつ),*args(位置引数), **kwargs（キーワード引数）) 　reverse()関数は、指定されたviewnameに対応するURLパターンのURL文字列を生成する

class RegisterDirectorView(generic.CreateView):
    model = Director
    form_class = DirectorForm
    template_name = 'myapp/register.html'
    def get_success_url(self):
        return reverse('myapp:registermovie') 

#新しい映画作品情報の作成
#kwargs(キーワード引数)={'pk': self.object.pk }) 新しく作成された映画のプライマリキーをpkパラメーターとして渡している

class RegisterMovieView(generic.CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'myapp/register.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # 現在のユーザーをuserフィールドに割り当てる
        return super().form_valid(form)


def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.movie = Movie.objects.get(pk=self.kwargs['movie_id'])
    return super(WritingLogView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('myapp:movie_detail', kwargs={'pk': self.object.pk }) 

#新しい感想の作成

class WritingLogView(generic.CreateView):
    model = Log
    form_class = LogForm
    template_name = 'myapp/register.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie = Movie.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


    def form_valid(self, form):
        form.instance.user = self.request.user  # ログインユーザーをログのユーザーに関連付ける
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('myapp:movie_detail', kwargs={'pk': self.object.movie.pk }) 

#編集後のアップデート
#UpdateViewは、既存のオブジェクトを更新するための汎用ビュー

class UpdateLogView(generic.UpdateView):
    model = Log
    form_class = LogForm
    template_name = "myapp/register.html"
    def get_success_url(self):
        return reverse('myapp:movie_detail', kwargs={'pk': self.object.movie.pk })

#ログのみ削除
#DeleteViewは、オブジェクトを削除するための汎用ビュー

class DeleteLogView(generic.DeleteView):
    model = Log
    template_name = 'myapp/movie_confirm_delete.html'
    def get_success_url(self):
        return reverse('myapp:movie_detail', kwargs={'pk': self.object.movie.pk})

#映画を削除（その映画のログも全部消える）

class DeleteMovieView(generic.DeleteView):
    model = Movie
    def get_success_url(self):
        return reverse('myapp:index')


#新規アカウント作成
    
class  AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
        # アカウント作成が成功したかどうかのフラグ
        "AccountCreate":False,
        # アカウント情報を入力するためのフォーム
        "account_form": AccountForm(),
        }

    # Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["AccountCreate"] = False
        return render(request,"myapp/register2.html",context=self.params)

    # Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)

        # フォーム入力の有効検証
        if self.params["account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()


            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"myapp/register2.html",context=self.params)



#movie_id は、新しいログが作成される映画のプライマリキー
def writingthismovielog(request, pk):
    
    #指定されたモデル（ここでは Movie）からオブジェクトを取得。movie_id に対応する映画オブジェクトが存在しない場合は、HTTP 404 エラーを返す。
    obj = get_object_or_404(Movie, id=pk)
    
    #({'movie':obj}):LogForm movie フィールドには、obj（映画オブジェクト）を初期値として渡す
    form = LogForm(initial={'movie':obj})


    if request.method == "POST":

        #データを使用してログフォームを再作成
        form = LogForm(request.POST)
        
        #フォームの入力が妥当であるかどうかをチェック（必須項目が入力されているかなど）
        if form.is_valid():

            #フォームのデータをモデルオブジェクトに保存。データベースには保存せずに、一時的なオブジェクトとしてメモリに保持
            #この場合、新しいログオブジェクトが作成され、変数 l に割り当てられる
            l = form.save(commit=False)
            l.user = request.user  # ログインユーザーをログのユーザーに関連付ける
            l.movie = obj  
            #データベースに保存
            l.save()

            #ログが正常に作成された場合、そのログが関連付けられている映画の詳細ページにリダイレクト
     
            return redirect('myapp:movie_detail', pk=obj.pk)
    
    #POST メソッドでない場合、つまりフォームがまだ送信されていない場合は、ログフォームを含むページを表示
    else:
        return render(request, 'myapp/register.html', {'form': form})
    

#ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('myapp:home'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'myapp/login.html')


#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('myapp:Login'))

@login_required
def home(request):
    # ログ一覧を取得
    user_logs = Log.objects.filter(user=request.user)

    # テンプレートに渡すコンテキスト
    context = {
        'username': request.user.username,
        'user_logs': user_logs,
    }

    return render(request, "myapp/home.html", context=context)
