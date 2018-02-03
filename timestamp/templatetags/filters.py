from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='mon_to_text')
def mon_to_text(value): # Only one argument.
    print('filter=',value)
    month_text = [
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь',
    ]
    month_name=month_text[value-1]
    return month_name
