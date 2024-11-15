from django.urls import path
from .views import StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView
app_name='student'
from .views import student_companies_view
urlpatterns = [
    path('', StudentListView.as_view(), name='student_list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('new/', StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/edit/', StudentUpdateView.as_view(), name='student_update'),
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    path('<int:student_id>/companies/', student_companies_view, name='student_companies'),
]