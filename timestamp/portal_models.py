from calendar import monthrange
import datetime
from . import connector_django as connector
from django.db.models import Sum

class Month:
    def __init__(self, year, month,month_timestamps):
        self.dates = list()
        num_days = monthrange(year, month)[1]
        for day in range(1, num_days + 1):
            date=datetime.date(year, month, day)
            date_obj = DateOfMonth(date)
            date_ts=month_timestamps.filter(date=date)
            # Если на день есть отметки
            if date_ts.count()>0:
                date_obj.label_wait = True
                # Считаем сумму принятых отметок
                accepted_hours=date_ts.filter(status=1).aggregate(Sum('hours'))['hours__sum']
                # Если есть утвержденные отметки
                if not(accepted_hours==None):
                    if accepted_hours>8:
                        date_obj.label_overtime=True
                        date_obj.label_wait = False
                    elif accepted_hours==8:
                        date_obj.label_eight = True
                        date_obj.label_wait = False

                # Считаем количество отклоненных отметок
                rejected = date_ts.filter(status=2).count()
                if rejected>=1:
                    date_obj.label_reject=True
            self.dates.append(date_obj)


class DateOfMonth:
    def __init__(self, setdate):
        self.date = setdate
        self.label_eight=False
        self.label_wait=False
        self.label_reject=False
        self.label_overtime=False
        if setdate.weekday() in {5, 6}:
            self.isWeekend = True
        else:
            self.isWeekend = False

        self.label_eight = False
        self.label_no_ts = False
        self.label_rejected = False
        self.label_wait = False


class ProjectTasks:
    def __init__(self, user, date, timestamps):
        # TODO Задачи - это два множеста - задачи для отметки (на них можно отмечаться) и задачи, по которым отметка уже есть (по ним нельзя отмечаться, можно только смотреть)
        tasks, all_projects, all_stages = connector.get_project_tasks(user, date)
        project_list = tasks.order_by().values('project').distinct()
        self.projects = list()
        for project_item in project_list:
            project_id = project_item['project']
            project = Project(all_projects.get(id=project_id))
            stage_list = tasks.filter(project=project_id).order_by().values('stage').distinct()
            for stage_item in stage_list:
                stage_id = stage_item['stage']
                stage = Stage(all_stages.get(id=stage_id))
                task_list = tasks.filter(project=project_id, stage=stage_id)
                for task_item in task_list:
                    task = Task(task_item)
                    task.ts = timestamps.ts_db.filter(task_id=task_item.id, task_type=1)
                    stage.tasks.append(task)
                project.stages.append(stage)
            self.projects.append(project)


class Project:
    stages = list()

    def __init__(self, project):
        self.id = project.id
        self.name = project.name
        self.stages = list()

    def __str__(self):
        return 'project:' + str(self.id) + ' ' + self.name


class Stage:
    tasks = list()

    def __init__(self, stage):
        self.id = stage.id
        self.name = stage.name
        self.tasks = list()

    def __str__(self):
        return 'stage:' + str(self.id) + ' ' + self.name


class Task:
    def __init__(self, task):
        self.id = task.id
        self.name = task.name
        self.task_type = task.task_type

    def __str__(self):
        return str(self.id) + ' ' + self.name


class Timestamps:
    def __init__(self, user, date):
        self.ts_db = connector.get_timestamps(user, date)
        self.ts_queue = None


class CommonTasks:
    def __init__(self, timestamps):
        tasks, all_stages = connector.get_common_tasks()
        stages_list = tasks.order_by().values('stage').distinct()
        self.stages = list()
        for stage_item in stages_list:
            stage_id = stage_item['stage']
            stage = CommonStage(all_stages.get(id=stage_id))
            task_list = tasks.filter(stage=stage_id)
            for task_item in task_list:
                task = CommonTask(task_item)
                task.ts = timestamps.ts_db.filter(task_id=task_item.id, task_type=2)
                stage.tasks.append(task)
            self.stages.append(stage)


class CommonStage:
    def __init__(self, stage):
        self.id = stage.id
        self.name = stage.name
        self.tasks = list()


class CommonTask:
    def __init__(self, task):
        self.id = task.id
        self.name = task.name
        self.task_type = task.task_type

class QuartalTasks:
    def __init__(self, user, timestamps):
        task_list = connector.get_quartal_tasks(user)
        self.tasks=list()
        for task_item in task_list:
            task = QuartalTask(task_item)
            task.ts = timestamps.ts_db.filter(task_id=task_item.id, task_type=4)
            self.tasks.append(task)


class QuartalTask:
    def __init__(self, task):
        self.id = task.id
        self.name = task.name
        self.task_type = task.task_type