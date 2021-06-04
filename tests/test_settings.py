from django.test import TestCase

from graphql_extensions import settings


class SettingsTests(TestCase):

    def test_perform_import(self):
        f = settings.perform_import(id, '')
        self.assertEqual(f, id)

        f = settings.perform_import('django.test.TestCase', '')
        self.assertEqual(f, TestCase)

        f = settings.perform_import(['django.test.TestCase'], '')
        self.assertEqual(f, [TestCase])

    def test_import_from_string_error(self):
        with self.assertRaises(ImportError):
            settings.import_from_string('error', '')

    def test_reload_settings(self):
        getattr(settings.extensions_settings, 'SHOW_ERROR_MESSAGE_HANDLER')

        settings.reload_settings(setting='TEST')
        self.assertTrue(settings.extensions_settings._cached_attrs)

        settings.reload_settings(setting='GRAPHQL_EXTENSIONS')
        self.assertFalse(settings.extensions_settings._cached_attrs)
