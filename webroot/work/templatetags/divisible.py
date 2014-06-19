from django.template import Library
register = Library()

@register.filter
def divisible(num, by):
    return (num % by)
