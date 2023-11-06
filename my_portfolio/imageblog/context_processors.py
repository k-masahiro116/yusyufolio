from .models import UploadImage

def common(request):
    image_list = UploadImage.objects.order_by("-id")
    return {'image_list': image_list}