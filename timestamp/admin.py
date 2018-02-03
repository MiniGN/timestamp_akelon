from    django.contrib import admin
from .models import *

admin.site.register(TaskType)

class ProjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Project._meta.fields]
    class Meta:
        model=Project
admin.site.register(Project,ProjectAdmin)

class StageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProjectStage._meta.fields]
    class Meta:
        model=ProjectStage

admin.site.register(ProjectStage,StageAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProjectTask._meta.fields]
    class Meta:
        model=ProjectTask
admin.site.register(ProjectTask,TaskAdmin)

class TimestampAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TimestampTask._meta.fields]
    class Meta:
        model=TimestampTask
admin.site.register(TimestampTask,TimestampAdmin)


class TimestampStatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TimestampStatus._meta.fields]
    class Meta:
        model=TimestampStatus

admin.site.register(TimestampStatus,TimestampStatusAdmin)

admin.site.register(CommonStage)

class CommonTaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CommonTask._meta.fields]
    class Meta:
        model=CommonTask
admin.site.register(CommonTask,CommonTaskAdmin)

class QuartalTaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in QuartalTask._meta.fields]
    class Meta:
        model=QuartalTask
admin.site.register(QuartalTask,QuartalTaskAdmin)

