from django.shortcuts import render, get_object_or_404
from .models import Study


def index(request):
    return render(request, "core/index.html")


def study_detail(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    return render(request, "core/study/detail.html", {
        'study': study        
    })
