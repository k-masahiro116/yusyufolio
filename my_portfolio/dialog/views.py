import locale
locale.setlocale(locale.LC_ALL, '')
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.db.models import Q
from .chains import ChitChat, StrictTask, Detector, ConcatChain, Parse
from .hdsr import HDSR
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'dialog/index.html'
    
class UserdataListView(LoginRequiredMixin, generic.ListView):
    model = Userdata
    
class UserdataCreateView(generic.CreateView): # 追加
    model = Userdata # 作成したい model を指定
    form_class = UserdataCreateForm # 作成した form クラスを指定
    success_url = reverse_lazy('dialog:user_list')
    calc_model = HDSR()
    def post(self, request, *args, **kwargs):
        valid = super().post(request, *args, **kwargs)
        self.form = self.get_form()
        if self.form.instance.birth is not None:
            birth_date = timezone.datetime.strptime(str(self.form.instance.birth), '%Y-%m-%d').strftime('%Y%m%d')
            now_date = timezone.now().strftime('%Y%m%d')
            self.form.instance.age = (int(now_date) - int(birth_date)) // 10000
        if self.form.instance.hdsr.all() is not None:
            self.calc_score()
            scores = [hdsr.score for hdsr in self.form.instance.hdsr.all()]
            if scores != []:
                self.form.instance.max_score = max(scores)
                self.form.instance.min_score = min(scores)
        self.form.instance.user = self.request.user
        self.form_valid(self.form)
        return valid
    
    def calc_score(self):
        for hdsr in self.form.instance.hdsr.all():
            ymdA = [
                hdsr.date.strftime('%Y年'),
                hdsr.date.strftime('%m月'),
                hdsr.date.strftime('%d日'),
                hdsr.date.strftime('%A')
            ]
            self.calc_model.set_refer_data({
                "居場所": [self.form.instance.place], 
                "年齢": [self.form.instance.age], 
                "年月日曜日": ymdA})
            hdsr_dict = hdsr.return_self()
            slot_score = self.calc_model(hdsr_dict)
            hdsr.set_score_from_dict(slot_score)
    
class UserdataDetailView(generic.DetailView): 
    model = Userdata 
    
class UserdataUpdateView(generic.UpdateView): 
    model = Userdata
    form_class = UserdataCreateForm 
    success_url = reverse_lazy('dialog:user_list')
    calc_model = HDSR()
    def post(self, request, *args, **kwargs):
        valid = super().post(request, *args, **kwargs)
        self.form = self.get_form()
        if self.form.instance.birth is not None:
            birth_date = timezone.datetime.strptime(str(self.form.instance.birth), '%Y-%m-%d').strftime('%Y%m%d')
            now_date = timezone.now().strftime('%Y%m%d')
            self.form.instance.age = (int(now_date) - int(birth_date)) // 10000
        if self.form.instance.hdsr.all() is not None:
            self.calc_score()
            scores = [hdsr.score for hdsr in self.form.instance.hdsr.all()]
            if scores != []:
                self.form.instance.max_score = max(scores)
                self.form.instance.min_score = min(scores)
        self.form_valid(self.form)
        return valid
    
    def calc_score(self):
        for hdsr in self.form.instance.hdsr.all():
            ymdA = [
                hdsr.date.strftime('%Y年'),
                hdsr.date.strftime('%m月'),
                hdsr.date.strftime('%d日'),
                hdsr.date.strftime('%A')
            ]
            self.calc_model.set_refer_data({
                "居場所": [self.form.instance.place], 
                "年齢": [self.form.instance.age], 
                "年月日曜日": ymdA})
            hdsr_dict = hdsr.return_self()
            slot_score = self.calc_model(hdsr_dict)
            hdsr.set_score_from_dict(slot_score)
            
class UserdataDeleteView(generic.DeleteView): # 追加
    model = Userdata
    success_url = reverse_lazy('dialog:user_list')
    
class EvaluationView(LoginRequiredMixin, generic.ListView):
    template_name = 'dialog/evaluation.html'
    model = HDSR_Model
    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word:
            object_list = HDSR_Model.objects.filter(
                Q(name__icontains=q_word) | Q(date__icontains=q_word) | Q(score__icontains=q_word))
        else:
            object_list = HDSR_Model.objects.all()
        return object_list
    
class EvaluationDetailView(generic.DetailView):
    template_name = 'dialog/evaluation_detail.html'
    model = HDSR_Model
    chain = Parse()
    calc_model = HDSR()
    def get_context_data(self,**kwargs):
        if not self.object.asigned:
            self.input_HDSR_Model()
        context = super().get_context_data(**kwargs)
        post_list = []
        for post in Post.objects.filter(index=self.object):
            post_list.append(post)
        context.update({"post_list": post_list})
        return context
    
    def input_HDSR_Model(self):
        hdsr_text = ""
        for post in Post.objects.filter(index=self.object):
            hdsr_text = hdsr_text+"\n{0}:{1}".format(post.speaker, post.text)
        def parse(hdsr_text):
            text = self.chain.run(hdsr_text)
            l = text.split("\n")
            hdsr_dict = {}
            for i in l:
                hdsr_text = i.replace(" ", "")
                key, value = hdsr_text.split(":")
                hdsr_dict[key] = value
            return hdsr_dict
        try:
            hdsr_dict = parse(hdsr_text)
        except:
            hdsr_dict = {}
        self.object.set_from_dict(hdsr_dict)
        
class EvaluationDeleteView(generic.DeleteView): 
    template_name = 'dialog/evaluation_delete.html'
    model = HDSR_Model
    success_url = reverse_lazy('dialog:evaluation')
    
class EvaluationUpdateView(generic.UpdateView): 
    template_name = 'dialog/evaluation_form.html'
    model = HDSR_Model
    form_class = EvalCreateForm
    success_url = reverse_lazy('dialog:evaluation')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        score = 0
        for key in form.data:
            if "score" in key:
                score += int(form.data.get(key))
        form.instance.score = score
        form.save()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        post_list = []
        for post in Post.objects.filter(index=self.object):
            post_list.append(post)
        context.update({"post_list": post_list})
        return context
    def get_success_url(self):
        return reverse_lazy('dialog:evaluation_detail', kwargs={'pk': self.kwargs['pk']})
    
class PostCreateView(generic.CreateView): # 追加
    model = Post # 作成したい model を指定
    form_class = PostCreateForm # 作成した form クラスを指定
    chain = ConcatChain(chitchat=ChitChat(), detector=Detector(), strict=StrictTask())
    success_url = reverse_lazy('dialog:post_list')
    model_name = ""
    last_index = -1
    def post(self, request, *args, **kwargs):
        if list(filter(None, Post.objects.all())) != []:
            self.last_index = Post.objects.all().last().index
        valid = super().post(request, *args, **kwargs)
        self.eldely_care_llms()
        return valid
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def eldely_care_llms(self):
        form = self.get_form()
        if self.request.user == AnonymousUser() or self.request.user == None:
            user = get_user_model().objects.get(username="anonymous")
        else:
            user = self.request.user
        form.instance.user = user
        index = None
        response = self.chain.run(form.instance.text)
        if self.chain.pre_model == self.chain.model and self.chain.model == "strict":
            index = self.next_index(user)
            form.instance.index = index
        self.form_valid(form)
        Post.objects.create(speaker="ワンコ", text=response, index=index, user=user)
        
    def next_index(self, user):
        if self.last_index == None:
            obj = HDSR_Model.objects.create()
            obj.user = user
            return obj
        else:
            return self.last_index
            
class PostListView(LoginRequiredMixin, generic.ListView):
    template_name = 'dialog/post_list_anime.html'
    model = Post
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        def get_last_post():
            obj = self.object_list[len(self.object_list)-1] if len(self.object_list) > 0 else Post()
            return {"last_post": "'"+obj.text.replace("\n", "")+"'", "last_date": obj.date}
            
        context.update(get_last_post())
        return context

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word:
            object_list = Post.objects.filter(
                Q(speaker__icontains=q_word) | Q(text__icontains=q_word) | Q(date__icontains=q_word))
        else:
            object_list = Post.objects.all()
        return object_list

class PostDetailView(generic.DetailView): 
    model = Post  # pk(primary key)はurls.pyで指定しているのでここではmodelを呼び出すだけで済む
    
class PostUpdateView(generic.UpdateView): 
    model = Post
    form_class = PostCreateForm # PostCreateFormをほぼそのまま活用できる
    success_url = reverse_lazy('dialog:post_list')
    
class PostDeleteView(generic.DeleteView): 
    model = Post
    success_url = reverse_lazy('dialog:post_list')
    
