from .models import *

def get_project_tasks(user, date):
    # TODO Фильтрация задач по пользователю
    selected_tasks=ProjectTask.objects.filter(start__lte=date, end__gte=date)
    all_projects=Project.objects.all()
    all_stages=ProjectStage.objects.all()
    return selected_tasks,all_projects,all_stages

def get_common_tasks():
    selected_tasks=CommonTask.objects.filter()
    all_stages=CommonStage.objects.all()
    return selected_tasks,all_stages

def get_quartal_tasks(user):
    selected_tasks=QuartalTask.objects.filter()
    return selected_tasks


def get_timestamps(focus_user,date):
    ts=TimestampTask.objects.filter(user=focus_user,date=date)
    return ts