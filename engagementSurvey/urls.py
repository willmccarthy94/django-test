from django.urls import path
from django.conf.urls import url

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
]

app_name = 'engagementSurvey'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name ='new'),
    path('<str:company_name>/results/', views.results, name='results'),
    path('<str:company_name>/export/', views.export_answers_csv, name='export_answers_csv'),
    path('<str:company_name>/<str:secret_id>/', views.landing, name = 'landing'),
    path('<str:company_name>/<str:secret_id>/survey/', views.survey, name = 'survey'),
    path('<str:company_name>/<str:secret_id>/thanks/', views.thanks, name = 'thanks'),
    path('<str:company_name>/<str:secret_id>/submit/', views.submit, name ='submit'),
]