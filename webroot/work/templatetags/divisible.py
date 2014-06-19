from django.template import Library
register = Library()

@register.filter
def divisible(num, by):
    print "{0} \% {1} = {2}".format(num, by, num % by)
    return (num % by)
