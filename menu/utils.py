from django.core.cache import cache
from .models import MenuItem


def get_menu_data(menu_slug, current_path):
    cache_key = f'menu_{menu_slug}_{current_path}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    items = list(MenuItem.objects.filter(
        menu__slug=menu_slug
    ).select_related('parent').order_by('order'))

    items_dict = {item.id: item for item in items}
    root_items = []

    for item in items:
        item.expanded = False
        item_url = item.get_url
        item.active = current_path.startswith(item_url)

        if item.parent is None:
            root_items.append(item)
        else:
            parent = items_dict.get(item.parent_id)
            if parent:
                if not hasattr(parent, 'children_list'):
                    parent.children_list = []
                parent.children_list.append(item)

    _mark_expanded(root_items, current_path)
    cache.set(cache_key, root_items, 3600)
    return root_items


def _mark_expanded(items, current_path):
    for item in items:
        if hasattr(item, 'children_list'):
            if not hasattr(item, 'expanded'):
                item.expanded = False
            for child in item.children_list:
                _mark_expanded([child], current_path)
            item.expanded = item.active or any(
                child.active or child.expanded 
                for child in item.children_list
            )
    return any(getattr(item, 'expanded', False) for item in items)
