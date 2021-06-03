from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    'SHOW_ERROR_MESSAGE_HANDLER':
    'graphql_extensions.views.show_error_message',
}

IMPORT_STRINGS = (
    'SHOW_ERROR_MESSAGE_HANDLER',
)


def perform_import(value, setting_name):
    if isinstance(value, str):
        return import_from_string(value, setting_name)
    if isinstance(value, (list, tuple)):
        return [import_from_string(item, setting_name) for item in value]
    return value


def import_from_string(value, setting_name):
    try:
        return import_string(value)
    except ImportError as e:
        msg = (
            f'Could not import `{value}` for EXTENSIONS setting'
            f'`{setting_name}`. {e.__class__.__name__}: {e}.'
        )
        raise ImportError(msg)


class ExtensionsSettings(object):

    def __init__(self, defaults, import_strings):
        self.defaults = defaults
        self.import_strings = import_strings
        self._cached_attrs = set()

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f'Invalid setting: `{attr}`')

        value = self.user_settings.get(attr, self.defaults[attr])

        if attr in self.import_strings:
            value = perform_import(value, attr)

        self._cached_attrs.add(attr)
        setattr(self, attr, value)
        return value

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'GRAPHQL_EXTENSIONS', {})
        return self._user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)

        self._cached_attrs.clear()

        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


def reload_settings(*args, **kwargs):
    setting = kwargs['setting']

    if setting == 'GRAPHQL_EXTENSIONS':
        extensions_settings.reload()


setting_changed.connect(reload_settings)

extensions_settings = ExtensionsSettings(DEFAULTS, IMPORT_STRINGS)
