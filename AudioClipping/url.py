from django.urls import path
from . import views

urlpatterns=[
    path('clipping',views.index2,name='clipping'),
    path('clippingdone', views.AudioClipping, name="clippingdone"),
    path('Audiocadstart', views.AudioClippingAdminStart, name="Audiocadstart")


]
