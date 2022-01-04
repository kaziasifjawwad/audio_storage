from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('upload',views.upload,name='upload'),
    path('result',views.result,name='result'),
    path('getfiles',views.getFiles, name = "fetfiles"),
    path('delete/<file_id>',views.deleteFiles,name='delete'),
    path('dataset',views.dataset,name="dataset")
]
