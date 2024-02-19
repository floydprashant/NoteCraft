from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('image2text', views.image2text, name="image2text"),
    path('text2QNA', views.text2QNA, name="text2QNA")
]
