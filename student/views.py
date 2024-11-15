
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Student

class StudentListView(ListView):
    model = Student
    template_name = 'student/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        # Get all students and order by batch_code
        queryset = Student.objects.all().order_by('batch_code')
        
        # Group students by batch_code
        batch_groups = {}
        for student in queryset:
            batch_code = student.batch_code
            if batch_code not in batch_groups:
                batch_groups[batch_code] = []
            batch_groups[batch_code].append(student)
        
        return batch_groups

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'student'

class StudentCreateView(CreateView):
    model = Student
    template_name = 'student/student_form.html'
    fields ='__all__'
    success_url = reverse_lazy('student:student_list')

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'student/student_form.html'
    fields = '__all__'
    success_url = reverse_lazy('student:student_list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student/student_confirm_delete.html'
    success_url = reverse_lazy('student:student_list')


from django.shortcuts import render, get_object_or_404
from .models import Student
from company.models import Company

def student_companies_view(request, student_id):
    # Get the student instance
    student = get_object_or_404(Student, pk=student_id)

    # Get all companies associated with the student
    companies = student.companies.all()

    # Calculate the total number of companies and the number of scheduled companies
    total_companies = companies.count()
    total_scheduled = companies.filter(is_scheduled=True).count()

    context = {
        'student': student,
        'companies': companies,
        'total_companies': total_companies,
        'total_scheduled': total_scheduled,
    }

    return render(request, 'student/student_companies.html', context)
