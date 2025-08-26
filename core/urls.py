from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('study_list_items', views.study_list_items, name='study_list_items'),
    path("study/<int:study_id>/", views.study_detail, name="study_detail"),
    path("study/<int:study_id>/donation-modal/<int:service_id>", views.study_donation_modal, name="study_donation_modal"),
    path("study/<int:study_id>/donation-complete-modal", views.study_donation_complete_modal, name="study_donation_complete_modal"),
    path(
        "study/<int:study_id>/connect/<int:service_id>",
        views.study_connect,
        name="study_connect"
    ),
    path("callback/<transfer_service_name>", views.callback, name="callback")
]
