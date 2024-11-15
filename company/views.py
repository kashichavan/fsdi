from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Company
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



