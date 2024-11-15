import pandas as pd
from django.core.exceptions import ValidationError
from .models import Student

def add_students_from_excel(company, excel_file):
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file, engine='openpyxl')

        # Check if required columns exist
        if 'name' not in df.columns or 'ph_no' not in df.columns:
            raise ValidationError("Excel file must contain 'name' and 'ph_no' columns.")

        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            name = row['name']
            ph_no = row['ph_no']

            # Try to get the student by phone number
            try:
                student = Student.objects.get(ph_no=ph_no)
            except Student.DoesNotExist:
                # If student does not exist, return a message
                return f"Student with phone number {ph_no} does not exist. Please add the student first."

            # Add the student to the company
            company.students.add(student)

        return "Students successfully added to the company."

    except Exception as e:
        raise ValidationError(f"An error occurred: {e}")
