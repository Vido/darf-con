from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from . import models

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='area_contador/resumo.html'), name='resumo'),
]
