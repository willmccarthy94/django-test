from django.db import models

# Create your models here.

class Question(models.Model):
    question_id = models.CharField(max_length = 10)
    question_text = models.CharField(max_length = 200)
    question_detail = models.CharField(max_length = 200)
    has_info_box = models.BooleanField(default = True)
    QUESTION_TYPES = ( #could have these as subclasses
        ('G','1-7 Gallup'),
        ('GP','1-7 Gallup with text box'),
        ('TB','Text box'),
        ('SO','Single option'),
        ('MO','Multiple option'),
    )
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES, default = 'G')

    def __str__(self):
        return self.question_text


class Company(models.Model):
    company_name =  models.CharField(max_length = 50)
    questions = models.ManyToManyField(Question)
    
    def __str__(self):
        return self.company_name


class Employee(models.Model):
    eid = models.CharField(max_length = 10)
    secret_id = models.CharField(max_length = 10, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    has_answered = models.BooleanField(default=False)
    answer_time = models.DateTimeField(blank=True)
    #temporary solution for employee types
    EMPLOYEE_TYPES = (
        ('UM','Upper Management'),
        ('MM','Middle Management'),
        ('LM','Lower Management'),
        ('OT','Other'),
    )
    e_type = models.CharField(max_length=2, choices=EMPLOYEE_TYPES, blank=True)

    #temporary solution for company division (add specific ones for companies later)
    EMPLOYEE_AREA = (
        ('E','Education'),
        ('HR','Human Resources'),
        ('F','Finance'),
        ('M','Management'),
        ('O','Other'),
    )
    job_area = models.CharField(max_length=2, choices=EMPLOYEE_AREA, blank=True)

    def __str__(self):
        return(self.company + ' ' + self.eid)


# Many different ways of storing this info. Not sure if best to have own table, or store elsewhere
class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    answer_value = models.SmallIntegerField(default=0)
    answer_text = models.CharField(max_length=600, blank=True)
    
    def __str__(self):
        return(self.answer_value)

#class CompanyAnswers(models.Model):
