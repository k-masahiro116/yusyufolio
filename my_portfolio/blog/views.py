from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import PostCreateForm
from .models import Post 
from django.db.models import Q

# Create your views here.
from django.views import generic
from django.shortcuts import redirect

class IndexView(generic.TemplateView):
    template_name = 'blog/index.html'
    
def redirect_view(request):
    models = Post.objects.all()
    model = models.last()
    if len(models) > 0:
        url = "post_detail/{}".format(model.pk)
        return redirect(url)
    else:
        return redirect("post_list")
    
class PostSidebarView(generic.ListView): # generic の ListViewクラスを継承
    model = Post # 一覧表示させたいモデルを呼び出し
    
class PostListView(generic.ListView): # generic の ListViewクラスを継承
    model = Post # 一覧表示させたいモデルを呼び出し
    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word:
            object_list = Post.objects.filter(
                Q(title__icontains=q_word) | Q(text__icontains=q_word) | Q(date__icontains=q_word) | Q(category__icontains=q_word))
        else:
            object_list = Post.objects.all()
        return object_list
    
class PostCreateView(generic.CreateView): # 追加
    model = Post # 作成したい model を指定
    form_class = PostCreateForm # 作成した form クラスを指定
    success_url = reverse_lazy('blog:post_list') # 記事作成に成功した時のリダイレクト先を指定
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        return context

class PostDetailView(generic.DetailView): # 追加
    model = Post  # pk(primary key)はurls.pyで指定しているのでここではmodelを呼び出すだけで済む
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        objects = Post.objects.order_by()
        
        index = list(objects).index(object)
        if len(objects) > index+1:
            obj = list(objects)[index+1]
            context["next_pk"] = obj.pk
            context["next_title"] = obj.title
        else:
            context["next_pk"] = object.pk
        if index-1 >= 0:
            obj = list(objects)[index-1]
            context["pre_pk"] = obj.pk
            context["pre_title"] = obj.title
        else:
            context["pre_pk"] = object.pk
        return context
        
    
class PostUpdateView(generic.UpdateView): # 追加
    model = Post
    form_class = PostCreateForm # PostCreateFormをほぼそのまま活用できる
    success_url = reverse_lazy('blog:post_list')
    
class PostDeleteView(generic.DeleteView): # 追加
    model = Post
    success_url = reverse_lazy('blog:post_list')
    
