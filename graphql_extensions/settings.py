from importlib import import_module

from django.conf import settings
from django.test.signals import setting_changed

DEFAULTS = {
    'EXT_SHOW_ERROR_MESSAGE_HANDLER':
    'graphql_extensions.views.show_error_message',
}

IMPORT_STRINGS = (
    'EXT_SHOW_ERROR_MESSAGE_HANDLER',
)


def perform_import(value, setting_name):
    if value is not None and isinstance(value, str):
        return import_from_string(value, setting_name)
    return value


def import_from_string(value, setting_name):
    try:
        module_path, class_name = value.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = 'Could not import `{}` for EXT setting `{}`. {}: {}.'.format(
            value, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class ExtensionsSettings(object):

    def __init__(self, defaults, import_strings):
        self.defaults = defaults
        self.import_strings = import_strings
        self._cached_attrs = set()

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError('Invalid setting: `{}`'.format(attr))

        value = self.user_settings.get(attr, self.defaults[attr])

        if attr in self.import_strings:
            value = perform_import(value, attr)

        self._cached_attrs.add(attr)
        setattr(self, attr, value)
        return value

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'GRAPHQL_EXT', {})
        return self._user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)

        self._cached_attrs.clear()

        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


def reload_settings(*args, **kwargs):
    setting = kwargs['setting']

    if setting == 'GRAPHQL_EXT':
        extensions_settings.reload()


setting_changed.connect(reload_settings)

extensions_settings = ExtensionsSettings(DEFAULTS, IMPORT_STRINGS)
