# urls.py

from django.urls import path
from .views import (
    CompanyListView,
    CompanyDetailView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView
)
from .views import upload_students_excel,add_student_to_company

app_name='company'

urlpatterns = [
    path('', CompanyListView.as_view(), name='company_list'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('new/', CompanyCreateView.as_view(), name='company_create'),
    path('<int:pk>/edit/', CompanyUpdateView.as_view(), name='company_update'),
    path('<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),
    path('companies/upload_students/<int:company_id>/', upload_students_excel, name='upload_students_excel'),
    path('<int:company_id>/add_student/', add_student_to_company, name='add_student_to_company'),
]
