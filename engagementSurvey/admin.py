from django.contrib import admin

# Register your models here.

from .models import Question, Company, Employee, Answer

admin.site.register(Question)
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Answer)