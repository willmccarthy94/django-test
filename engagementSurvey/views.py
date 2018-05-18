from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.urls import reverse
from datetime import datetime
from .forms import EmployeeForm, NewCompanyForm
from django.contrib.auth.decorators import login_required

import uuid
import random
import csv

# Create your views here.

from .models import Question, Company, Answer, Employee

def index(request):
    return HttpResponse("Hello, world. You're at the Engagement Survey Index")

'''
def landing(request,company_name,secret_id):
    company = get_object_or_404(Company, company_name=company_name)
    return render(request, 'engagementSurvey/landing.html', {'company': company})
'''

def survey(request,company_name,secret_id):
    company = get_object_or_404(Company, company_name=company_name)
    company_questions = company.questions.all()
    context = {
        'company_questions': company_questions,
        'company_name': company_name,
        'secret_id': secret_id,
    }
    return render(request, 'engagementSurvey/survey.html', context)

def thanks(request,company_name,secret_id):
    company = get_object_or_404(Company, company_name=company_name)
    return render(request, 'engagementSurvey/thanks.html', {'company_name': company_name})


# All needs changing!
def submit(request, company_name, secret_id):
    company = get_object_or_404(Company, company_name=company_name)
    questions = company.questions.all()
    employee = get_object_or_404(Employee, secret_id=secret_id)

    for question in questions:
        selected_choice = request.POST.get(str(question.question_id), "")
        submitted_answer_text = request.POST.get((str(question.question_id) + '_text'), "")
        if(not(submitted_answer_text == question.default_text)):
            answer = Answer(question=question, employee=employee, answer_value=selected_choice, answer_text=submitted_answer_text, company=company)
        else:
            answer = Answer(question=question, employee=employee, answer_value=selected_choice, company=company)
        answer.save()
        company.responses.add(answer)
        company.save()

    employee.has_answered=True
    employee.answer_time=datetime.now()
    employee.save()

    return HttpResponseRedirect(reverse('engagementSurvey:thanks',args=(company_name,secret_id,))) 

def landing(request,company_name, secret_id):
    
    company = get_object_or_404(Company, company_name=company_name)
    employee = get_object_or_404(Employee, secret_id=secret_id)

    if not(employee.has_answered):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = EmployeeForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                employee.e_type = form.cleaned_data['employee_type']
                employee.job_area = form.cleaned_data['employee_department']
                employee.save()
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('engagementSurvey:survey', kwargs=({'company_name' : company_name, 'secret_id': secret_id})))
        # if a GET (or any other method) we'll create a blank form
        else:
            form = EmployeeForm()
        context = {
            'form': form,
            'company_name': company_name,
            'secret_id': secret_id,
            'company': company,
        }
        
        return render(request, 'engagementSurvey/landing.html', context)    
    else:
        return HttpResponse("You've already answered this survey!")
    

@login_required
def results(request, company_name):
    company = get_object_or_404(Company, company_name=company_name)

    company_employees = Employee.objects.filter(company=company)
    company_questions = company.questions.all()
    company_employees_answered = Employee.objects.filter(company=company, has_answered=True)
    company_answers = Answer.objects.filter(company=company)

    company_employees_answered_count = str(len(company_employees_answered)) + "/" + str(len(company_employees))


    context = {
        'company_name': company_name,
        'company_employees': company_employees,
        'company_questions': company_questions,
        'company_employees_answered': company_employees_answered,
        'company_employees_answered_count': company_employees_answered_count,
        'company_answers': company_answers,

    }


    return render(request, 'engagementSurvey/results.html', context)    

def generateSecretId(company_code, employee_number):
    return str(company_code + str(employee_number) + str(random.randint(10000,99999)))

@login_required
def new(request):

    if request.method == 'POST':

        # New Company
        form = NewCompanyForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required
            company_name = form.cleaned_data['company_name']
            company_code = form.cleaned_data['company_code']
            num_employees = form.cleaned_data['num_employees']
            cid = str(uuid.uuid4())
            company = Company(company_name = company_name, company_code = company_code, num_employees=num_employees, cid=cid)
            company.save()
            e = 0
            while e < num_employees:
                eid = company_code + str(e)
                secret_id = generateSecretId(company_code,e)
                employee = Employee(eid=str(uuid.uuid4()), secret_id=secret_id, company=company)
                employee.save()
                company.employees.add(employee)
                company.save()
                e += 1

            # redirect to a new URL:
            return HttpResponse("Company " + company_name + " created with " + str(num_employees) + " employees")
        # if a GET (or any other method) we'll create a blank form
        
    else:
        form = NewCompanyForm()

    context = {
        'form': form,
    }
    
    return render(request, 'engagementSurvey/new.html', context)  
    

@login_required
def export_answers_csv(request, company_name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+ company_name + '_answers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Question', 'Employee', 'Value', 'Comment'])
    
    company = get_object_or_404(Company, company_name=company_name)
    answers = Answer.objects.filter(company=company).values_list('question__question_text','employee__secret_id','answer_value','answer_text')
    for answer in answers:
        writer.writerow(answer)

    return response