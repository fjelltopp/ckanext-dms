import ckan.logic as logic
import ckan.model as model
from ckan.common import c, request, is_flask_request

# for datetime string conversion
from datetime import datetime


def get_dataset_from_id(id):
    context = {
        'model': model, 'ignore_auth': True,
        'validate': False, 'use_cache': False
    }
    package_show_action = logic.get_action('package_show')
    return package_show_action(context, {'id': id})


def get_facet_items_dict(
        facet, search_facets=None, limit=None, exclude_active=False):
    '''Overwrite of core CKAN helper in order to get custom sorting order
    on some of the facets.

    Arguments:
    facet -- the name of the facet to filter.
    search_facets -- dict with search facets(c.search_facets in Pylons)
    limit -- the max. number of facet items to return.
    exclude_active -- only return unselected facets.

    '''
    if search_facets is None:
        search_facets = getattr(c, u'search_facets', None)

    if not search_facets \
       or not isinstance(search_facets, dict) \
       or not search_facets.get(facet, {}).get('items'):
        return []
    facets = []
    for facet_item in search_facets.get(facet)['items']:
        if not len(facet_item['name'].strip()):
            continue
        params_items = request.params.items(multi=True) \
            if is_flask_request() else request.params.items()
        if not (facet, facet_item['name']) in params_items:
            facets.append(dict(active=False, **facet_item))
        elif not exclude_active:
            facets.append(dict(active=True, **facet_item))
    # Replace CKAN default sort method
    facets = _facet_sort_function(facet, facets)
    if hasattr(c, 'search_facets_limits'):
        if c.search_facets_limits and limit is None:
            limit = c.search_facets_limits.get(facet)
    # zero treated as infinite for hysterical raisins
    if limit is not None and limit > 0:
        return facets[:limit]
    return facets


def _facet_sort_function(facet_name, facet_items):
    if facet_name == 'year':
        # Custom sort of year facet
        facet_items.sort(key=lambda it: it['display_name'].lower(), reverse=True)
    else:
        # Default CKAN sort: Sort descendingly by count and ascendingly by case-sensitive display name
        facet_items.sort(key=lambda it: (-it['count'], it['display_name'].lower()))
    return facet_items

def get_recently_updated():
    try:
        return logic.get_action('package_search')(
            data_dict={'q': '*:*', 'sort': 'metadata_modified desc', 'rows': 3})['results']
    except Exception as e:
        return []


def get_time_diff_in_hours(datetime_str):
    try:
        last_modified = datetime.fromisoformat(datetime_str)
        return (datetime.now() - last_modified).seconds // 3600
    except:
        pass
    return ""

def get_user_from_id(userid):
    try:
        user_show_action = logic.get_action('user_show')
        user_info = user_show_action({"include_password_hash": False, "include_password_hash": False}, {"id": userid})
        return user_info['fullname']
    except:
        pass
    return ""

def get_all_groups():
    try:
        return logic.get_action('group_list')(
                data_dict={'sort': 'title asc', 'all_fields': True})
    except:
        pass
    return ""
