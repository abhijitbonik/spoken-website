# Template tag used in watch_tutorial.html and tutorial_search.html.
# Used to check if item is in dict or not.

from django import template

register = template.Library()

def get_item(dictionary, key):
    return dictionary.get(str(key))  # returns None if key not found


register.filter('get_item', get_item)
