from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('show/<int:module_id>/', views.module, name='module'),
    path('attribute/<attr_id>/', views.dependency, name='dependency'),
    path('attribute/<attr_id>/dependency_ajax', views.dependency_ajax, name='dependency_ajax'),
    path('attribute/<attr_id>/dependent_ajax', views.dependent_ajax, name='dependent_ajax')
]
