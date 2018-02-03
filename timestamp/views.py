
from django.http import JsonResponse
from django.shortcuts import render,HttpResponseRedirect,render_to_response
# from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import connection
from datetime import datetime as dt
from django.utils import formats
import datetime
from calendar import monthrange
from . import portal_models
from django.views.decorators.csrf import csrf_exempt

def async_update_panels(request):
    focus_user=request.user
    focus_date=request.GET.get('date')

    focus_date=dt.strptime(focus_date,"%Y-%m-%d")

    # Отметки
    timestamps=portal_models.Timestamps(focus_user,focus_date)
    # Проектные задачи пользователя
    project_tasks=portal_models.ProjectTasks(focus_user,focus_date,timestamps)
    # Общекорп. задачи пользователя
    common_tasks=portal_models.CommonTasks(timestamps)
    # Квартальные задачи пользователя
    quartal_tasks = portal_models.QuartalTasks(focus_user,timestamps)

    return render_to_response('panels.html', {'project_tasks': project_tasks,'common_tasks':common_tasks,'quartal_tasks':quartal_tasks,'focus_date':focus_date})

def async_update_navbar(request):
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    nav = request.GET.get('nav')
    focus_user=request.user
    focus_year = year
    if nav=='left':
        focus_month = month -1
        if focus_month == 0:
            focus_month=12
            focus_year-=1
    else:
        focus_month = month +1
        if focus_month == 13:
            focus_month=1
            focus_year+=1

    month_timestamps=TimestampTask.objects.filter(user=focus_user,date__year=focus_year,date__month=focus_month)
    month=portal_models.Month(focus_year,focus_month,month_timestamps)

    return render_to_response('navbar.html', {'focus_year': focus_year,'focus_month':focus_month,'month':month})

@csrf_exempt
def SendTimestamp(request):
    return_dict=dict()
    data=request.POST
    print (data)

    ts=data.get("ts")
    desc=data.get("desc")
    focus_date=data.get("focus_date")

    task_id=data.get("task_id")
    task_type=data.get("task_type")
    focus_user = request.user
    status_obj=TimestampStatus.objects.get(id=3)
    task_type_obj=TaskType.objects.get(name=task_type)
    TimestampTask.objects.create(hours=ts,desc=desc,date=focus_date,task_id=task_id,task_type=task_type_obj,user=focus_user,status=status_obj)
    return JsonResponse(return_dict)

@csrf_exempt
def home(request):
    focus_date=dt.now()
    focus_year=focus_date.year
    focus_month=focus_date.month

    user=User.objects.get(id=2)
    login(request, user)
    focus_user=request.user

    month_timestamps=TimestampTask.objects.filter(user=focus_user,date__year=focus_year,date__month=focus_month)
    # Отметки
    timestamps=portal_models.Timestamps(focus_user,focus_date)
    # Календарь дат
    month=portal_models.Month(focus_year,focus_month,month_timestamps)
    # Проектные задачи пользователя
    project_tasks=portal_models.ProjectTasks(focus_user,focus_date,timestamps)
    # Общекорп. задачи пользователя
    common_tasks=portal_models.CommonTasks(timestamps)
    # Квартальные задачи пользователя
    quartal_tasks = portal_models.QuartalTasks(focus_user,timestamps)

    # users = User.objects.filter(is_superuser=False)
    return render(request,'home.html',locals())
