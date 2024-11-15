from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Company
from student.models import Student
from django.core.exceptions import ValidationError

class CompanyListView(ListView):
    model = Company
    template_name = 'company/company_list.html'
    context_object_name = 'companies'

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company/company_detail.html'
    context_object_name = 'company'

class CompanyCreateView(CreateView):
    model = Company
    template_name = 'company/company_form.html'
    fields = ['name', 'company_code', 'is_scheduled', 'schedule_date']
    success_url = reverse_lazy('company:company_list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class CompanyUpdateView(UpdateView):
    model = Company
    template_name = 'company/company_form.html'
    fields = ['name', 'company_code', 'is_scheduled', 'schedule_date']
    success_url = reverse_lazy('company:company_list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'company/company_confirm_delete.html'
    success_url = reverse_lazy('company:company_list')


# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Company
from .utils import add_students_from_excel  # Import the function

def upload_students_excel(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')

        if not excel_file:
            messages.error(request, "No file selected.")
            return render(request, 'upload_students_excel.html', {'company': company, 'show_popup': True})

        try:
            # Call the utility function to process the Excel file
            result_message = add_students_from_excel(company, excel_file)

            if "does not exist" in result_message:
                # If the result contains a message indicating a missing student
                messages.error(request, result_message)
                return render(request, 'upload_students_excel.html', {'company': company, 'show_popup': True})
            
            messages.success(request, result_message)  # If students are successfully added
            return redirect('company:company_detail', pk=company.id)
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'upload_students_excel.html', {'company': company, 'show_popup': True})

    return render(request, 'upload_students_excel.html', {'company': company})
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Student, Company
from .forms import StudentPhoneNumberForm

def add_student_to_company(request, company_id):
    # Get the company object using the provided company_id
    company = get_object_or_404(Company, id=company_id)

    # Handle the POST request
    if request.method == 'POST':
        form = StudentPhoneNumberForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            
            try:
                # Try to retrieve the student by their phone number
                student = Student.objects.get(ph_no=phone_number)
            except Student.DoesNotExist:
                # If the student doesn't exist, show an error message
                messages.error(request, "This student is not registered in the database.")
                return redirect('company:add_student_to_company', company_id=company.id)
            
            # Check if the student is already associated with this company
            if student in company.students.all():
                messages.warning(request, "This student is already added to the company.")
            else:
                # Add the student to the company
                company.students.add(student)
                messages.success(request, f"Student {student.name} has been successfully added to the company.")
            
            # Redirect to the company detail page after successful operation
            return redirect('company:add_student_to_company', company_id=company.id)
        else:
            # If the form is not valid, show an error message
            messages.error(request, "Invalid phone number format. Please try again.")
    else:
        # If it's a GET request, create an empty form instance
        form = StudentPhoneNumberForm()

    # Render the template with the form and company context
    return render(request, 'company/add_student_to_company.html', {'form': form, 'company': company})
