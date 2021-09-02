import ckan.logic as logic
import ckan.model as model

def get_dataset_from_id(id):
    context = {
        'model': model, 'ignore_auth': True,
        'validate': False, 'use_cache': False
    }
    package_show_action = logic.get_action('package_show')
    return package_show_action(context, {'id': id})
