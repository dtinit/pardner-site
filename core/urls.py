from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("study/<int:study_id>/", views.study_detail, name="study_detail")
]
