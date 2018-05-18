from django import forms
from .models import Employee

class EmployeeForm(forms.Form):
    employee_type = forms.ChoiceField(choices=Employee.EMPLOYEE_TYPES)
    employee_department = forms.ChoiceField(choices=Employee.EMPLOYEE_AREA)

class NewCompanyForm(forms.Form):
    company_name = forms.CharField(max_length = 50)
    company_code = forms.CharField(max_length = 2)
    num_employees = forms.IntegerField()
