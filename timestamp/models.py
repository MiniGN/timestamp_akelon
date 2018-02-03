from django.db import models
from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User

class TaskType(models.Model):
    name=models.CharField(max_length=64)
    def __str__(self):
        return (self.name)

    class Meta:
        verbose_name='Тип задачи'
        verbose_name_plural='Типы задач'

class Project(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return 'Проект: %s' % (self.name)
class ProjectStage(models.Model):
    name = models.CharField(max_length=128)
    project = models.ForeignKey(Project)
    def __str__(self):
        return 'Этап: %s проекта:%s' % (self.name,self.project.name)
class ProjectTask(models.Model):
    name    = models.CharField(max_length=128)
    project = models.ForeignKey(Project)
    stage = models.ForeignKey(ProjectStage)
    start=models.DateField()
    end = models.DateField()
    executor = models.ForeignKey(User)
    task_type = models.ForeignKey(TaskType,blank=True)
    def __str__(self):
        return 'Проектная задача %s' % (self.name)
    def save (self,*args,**kwargs):
        type=TaskType.objects.get(name='project')
        self.task_type=type
        super(ProjectTask, self).save(*args, **kwargs)
    class Meta:
        verbose_name='Проектная задача'
        verbose_name_plural='Проектные задачи'

class CommonStage(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return 'Группа %s '% (self.name)
    class Meta:
        verbose_name = 'Группа постоянныех работ'
        verbose_name_plural = 'Группы постоянныех работ'
class CommonTask(models.Model):
    name    = models.CharField(max_length=128)
    stage = models.ForeignKey(CommonStage)
    task_type = models.ForeignKey(TaskType, blank=True)
    def __str__(self):
        return 'Работа %s' % (self.name)
    def save (self,*args,**kwargs):
        type=TaskType.objects.get(name='common')
        self.task_type=type
        super(CommonTask, self).save(*args, **kwargs)
    class Meta:
        verbose_name='Постоянная работа'
        verbose_name_plural='Постоянные работы'

class QuartalTask(models.Model):
    name    = models.CharField(max_length=128)
    executor = models.ForeignKey(User)
    task_type = models.ForeignKey(TaskType, blank=True)
    def __str__(self):
        return 'Кварт. задача %s' % (self.name)
    def save(self, *args, **kwargs):
        type = TaskType.objects.get(name='quartal')
        self.task_type = type
        super(QuartalTask, self).save(*args, **kwargs)
    class Meta:
        verbose_name='Квартальная задача'
        verbose_name_plural='Квартальные задачи'

class TimestampStatus(models.Model):
    name=models.CharField(max_length=64)
    class Meta:
        verbose_name='Статус отметок'
        verbose_name_plural='Статусы отметок'
    def __str__(self):
        return self.name

class TimestampTask(models.Model):
    hours = models.DecimalField(max_digits=5,decimal_places=2)
    desc=models.CharField(max_length=128)
    date=models.DateField()
    task_id=models.IntegerField()
    task_type=models.ForeignKey(TaskType)
    user=models.ForeignKey(User)
    status=models.ForeignKey(TimestampStatus)
    class Meta:
        verbose_name='Отметка'
        verbose_name_plural='Отметки'