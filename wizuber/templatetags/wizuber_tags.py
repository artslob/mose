from django import template

from wizuber.models import is_wizard

register = template.Library()

register.filter(is_wizard)
