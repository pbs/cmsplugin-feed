from django import template
import re

register = template.Library()


@register.filter(name='smart_truncate')
def smart_truncate(value, width):
    text = value.strip()
    if len(text) <= width:
        return text

    ellipsis = '...'
    text = text[:width]
    width = width - len(ellipsis)

    already_has_ellipsis = text.endswith(ellipsis)
    enough_space = width > 0

    if not enough_space or already_has_ellipsis:
        return text

    word_boundary = r'[\W\b\s]+'
    at_word_boundary = re.match(word_boundary, text[width-1:width+1])

    text = text[:width]
    if not at_word_boundary:
        # cut last word so that ellipsis is not shown in its middle
        no_last_word = re.split(word_boundary + r'\w*$', text)[0]
        # there might be a text with only one long word in which case
        #   leave it cut in the middle
        if no_last_word:
            text = no_last_word

    return text.strip() + ellipsis
