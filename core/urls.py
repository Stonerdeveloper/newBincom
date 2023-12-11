

from django.urls import path
from .views import ImageView, upload_image, custom_login,RegisterView, BaseView

urlpatterns = [
    path('image-list/', ImageView.as_view(), name='image_list'),
    path('upload/', upload_image, name='upload_image'),
    path('', custom_login, name='custom_login'),  
    path('base/', BaseView.as_view(), name='base'),
    path('register/', RegisterView.as_view(), name='register'),
]
