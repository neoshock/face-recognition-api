from django.urls import path
from .views import FaceDetectionView

urlpatterns= [
    path('face_detection/', FaceDetectionView.as_view(), name='list')
]