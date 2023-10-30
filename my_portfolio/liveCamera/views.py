from django.shortcuts import render, get_object_or_404
from .forms import UploadForm
from .models import UploadImage
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.views import generic
from django.http import HttpResponseRedirect

class IndexView(generic.TemplateView):
    template_name = 'liveCamera/index.html'
    
def image_upload(request):
    params = {
        'title': '画像のアップロード',
        'upload_form': UploadForm(),
        'id': None,
    }

    if (request.method == 'POST'):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_image = form.save()
            params['id'] = upload_image.id
        else:
            print(form)
            print(form.errors.as_text())

        return HttpResponseRedirect('/liveCamera/uploadimage_list')
    return render(request, 'liveCamera/image_upload.html', params)

def preview(request, image_id=0):
    
    upload_image = get_object_or_404(UploadImage, id=image_id)

    params = {
        'title': upload_image,
        'id': upload_image.id,
        'url': upload_image.image.url
    }

    return render(request, 'liveCamera/preview.html', params)

    
class ImageListView(generic.ListView): # generic の ListViewクラスを継承
    model = UploadImage # 一覧表示させたいモデルを呼び出し

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word:
            object_list = UploadImage.objects.filter(
                Q(title__icontains=q_word) | Q(id__icontains=q_word) | Q(date__icontains=q_word))
        else:
            object_list = UploadImage.objects.all()
        return object_list
    
class ImageDeleteView(generic.DeleteView): # 追加
    model = UploadImage
    success_url = reverse_lazy('liveCamera:uploadimage_list')
    