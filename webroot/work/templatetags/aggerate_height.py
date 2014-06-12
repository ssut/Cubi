# -*- coding: utf-8 -*-
from django.template import Library
register = Library()

@register.filter
def aggerate_height(list):
    return sum(image.image.height for image in list)

@register.filter
def calc_offset(self, index):
    offset = 0
    for i in range(1, index):
        offset += self[i - 1].image.height
    return offset
