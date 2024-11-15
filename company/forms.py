# forms.py
import re
from django import forms
from student.models import Student


class StudentPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label='Phone Number')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        # Strip spaces, dashes, or parentheses
        cleaned_phone_number = re.sub(r'[^0-9]', '', phone_number)

        # Validate phone number length (should be at least 10 digits)
        if len(cleaned_phone_number) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")

        # If the number has more than 10 digits, it might be valid for international formats
        if len(cleaned_phone_number) > 15:
            raise forms.ValidationError("Phone number is too long. Maximum length is 15 digits.")

        return cleaned_phone_number
