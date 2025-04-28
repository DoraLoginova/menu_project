from django import template
from django.utils.safestring import mark_safe
from ..models import MenuItem

register = template.Library()


@register.simple_tag
def draw_menu(menu_slug):
    root_items = MenuItem.objects.filter(
        menu__slug=menu_slug,
        parent__isnull=True
    ).order_by('order')
    return mark_safe(render_menu(root_items))


def render_menu(items, level=0):
    menu_html = '<ul class="menu-level-{}">'.format(level)
    for item in items:
        menu_html += '<li class="menu-item">'
        menu_html += '<a href="{}">{}</a>'.format(
            item.get_absolute_url,
            item.title
        )

        children = item.children.all()
        if children.exists():
            menu_html += render_menu(children, level+1)

        menu_html += '</li>'
    menu_html += '</ul>'
    return menu_html
