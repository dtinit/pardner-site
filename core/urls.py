from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("study/<int:study_id>/", views.study_detail, name="study_detail"),
    path(
        "study/<int:study_id>/connect/<transfer_service_name>",
        views.study_connect,
        name="study_connect"
    ),
    path("callback/<transfer_service_name>", views.callback, name="callback")
]
