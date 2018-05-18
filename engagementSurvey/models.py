from django.db import models

import uuid

# Create your models here.

class Question(models.Model):
    question_id = models.CharField(max_length=36,primary_key=True, default=str(uuid.uuid1()), editable=False)
    question_text = models.CharField(max_length = 200)
    question_detail = models.CharField(max_length = 200, blank=True)
    default_text = models.CharField(max_length = 50, default = "Add additional info")

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

    class Meta:
        ordering = ['question_type','question_text']

class Company(models.Model):
    cid = models.CharField(max_length=36, primary_key=True, default=str(uuid.uuid1()), editable=False)
    company_name =  models.CharField(max_length = 50)
    company_code = models.CharField(max_length = 2, unique=True)
    num_employees = models.IntegerField()
    questions = models.ManyToManyField(Question, blank=True)
    responses = models.ManyToManyField('Answer', blank=True)
    employees = models.ManyToManyField('Employee', blank=True, related_name='+')

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['company_name']
    
    def __str__(self):
        return self.company_name



class Employee(models.Model):
    eid = models.CharField(max_length=36, primary_key=True, default=str(uuid.uuid1()), editable=False)
    secret_id = models.CharField(max_length = 10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    has_answered = models.BooleanField(default=False)
    answer_time = models.DateTimeField(blank=True, null=True)
    #temporary solution for employee types
    EMPLOYEE_TYPES = (
        ('','- Level -'),
        ('UM','Upper Management'),
        ('MM','Middle Management'),
        ('LM','Lower Management'),
        ('OT','Other'),
    )
    e_type = models.CharField(max_length=2, choices=EMPLOYEE_TYPES, blank=True)

    #temporary solution for company division (add specific ones for companies later)
    EMPLOYEE_AREA = (
        ('','- Department -'),
        ('E','Education'),
        ('HR','Human Resources'),
        ('F','Finance'),
        ('M','Management'),
        ('O','Other'),
    )
    job_area = models.CharField(max_length=2, choices=EMPLOYEE_AREA, blank=True)

    def __str__(self):
        return(self.secret_id)

    class Meta:
        ordering = ['secret_id']


# Many different ways of storing this info. Not sure if best to have own table, or store elsewhere
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    answer_value = models.SmallIntegerField(default=0)
    answer_text = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['employee','question']

    def __str__(self):
        return((self.question.__str__()) + " " + self.employee.__str__() + ": " + str(self.answer_value) + ": " + str(self.answer_text))

    #Create new model methods to give easy access to questions and answers?
