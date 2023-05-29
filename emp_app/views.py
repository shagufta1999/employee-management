from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from emp_app.models import Employee


# Create your views here.
def index(request):
    return render(request,'index.html')

def add_emp(request):
    if request.method=='POST':
        first_name= request.POST['first_name']
        last_name = request.POST['last_name']
        bonus = int(request.POST['bonus'])
        salary = int(request.POST['salary'])
        phone = request.POST['phone']
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp=Employee(first_name=first_name,last_name=last_name,
                   bonus=bonus,salary=salary,phone=phone,
                   dept_id=dept,role_id=role,hire_date=datetime.now())
        new_emp.save()
        return HttpResponse("employee added successfully")
    elif request.method=='GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("error employee has not been added")



def all_emp(request):
    emps= Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request,'view_all_emp.html',context)

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed= Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse('Employee Removed Sucessfully')
        except:
            return HttpResponse("pls enter a valid emp id")

    emps=Employee.objects.all()
    context={
        'emps':emps
    }
    return render(request,'remove_emp.html',context)

def filter_emp(request):
    if request.method=='POST':
        name=request.POST['name']
        dept=request.POST['dept']
        role=request.POST['role']
        emps=Employee.objects.all()
        if name:
            emps= emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains= name))
        if dept:
            emps= emps.filter(dept__name= dept)
        if role:
            emps=emps.filter(role__name= role)
        context={
            'emps':emps
        }
        return render (request,'view_all_emp.html',context)
    elif request.method=='GET':
         return render(request,'filter_emp.html')
    else:
        return HttpResponse("An Exception Occured")