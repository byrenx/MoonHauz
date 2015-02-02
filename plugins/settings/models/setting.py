import ferris
from google.appengine.api import memcache
import logging
import datetime


class Setting(ferris.Model):
    _defaults = {}
    _settings = {}
    _settings_key = None
    _name = 'Unknown'

    class __metaclass__(ferris.Model.__metaclass__):
        def __new__(meta, name, bases, dict):
            cls = ferris.Model.__metaclass__.__new__(meta, name, bases, dict)

            if name != 'Setting':
                Setting._settings[ferris.inflector.underscore(cls.__name__)] = cls

                if name not in ('TimezoneSetting', 'EmailSetting', 'OAuth2Setting', 'UploadSetting', 'ServiceAccountSetting'):
                    from plugins.settings import is_active
                    if is_active():
                        logging.warning("Dynamic settings class %s loaded after the dynamic settings plugin was activated. Please check app/settings.py" % name)

            return cls

    @classmethod
    def factory(cls, name):
        return cls._settings[ferris.inflector.underscore(name)]

    @classmethod
    def _get_kind(cls):
        return '_ferris_setting_%s' % cls._settings_key

    @classmethod
    def get_key(cls):
        return ferris.ndb.Key(cls, cls._settings_key)

    @classmethod
    def get_instance(cls, static_settings=None):
        result = cls.get_instance_async().get_result()
        if not result:
            result = cls.get_default(defaults=static_settings, wait=True)
        return result

    @classmethod
    def get_default(cls, defaults=None, wait=True):
        cls_defaults = cls._defaults.copy()

        if defaults:
            cls_defaults.update(defaults.get(cls._settings_key, {}))

        result = cls(key=cls.get_key(), **cls_defaults)
        f = result.put_async()
        if wait:
            f.get_result()
        return result

    @classmethod
    def get_instance_async(cls):
        key = cls.get_key()
        return key.get_async()

    @classmethod
    def get_classes(cls):
        return cls._settings

    @classmethod
    @ferris.caching.cache_using_memcache('__ferris_settings')
    def get_settings(cls, static_settings):
        settings = {}

        # Gather all of the settings instances as futures
        futures = {}
        for k, settings_cls in cls._settings.iteritems():
            futures[settings_cls] = settings_cls.get_instance_async()

        # Wait for them to finish together
        ferris.ndb.Future.wait_all(futures.itervalues())

        # Transform them into dictionaries, using the default if needed.
        for settings_cls, future in futures.iteritems():
            value = future.get_result()
            if not value:
                value = settings_cls.get_default(defaults=static_settings, wait=False)

            settings[settings_cls._settings_key] = value.to_dict()

        logging.info("Dynamic settings loaded from datastore")

        return settings

    def after_put(self, key):
        memcache.delete('__ferris_settings')
        memcache.set('_ferris_settings_update_mutex', datetime.datetime.utcnow())


class TimezoneSetting(Setting):
    _name = 'Timezone'
    _settings_key = 'timezone'
    local = ferris.ndb.StringProperty(indexed=False)


class EmailSetting(Setting):
    _name = 'Email'
    _settings_key = 'email'
    sender = ferris.ndb.StringProperty(indexed=False)


class UploadSetting(Setting):
    _name = 'Upload'
    _settings_key = 'upload'
    use_cloud_storage = ferris.ndb.BooleanProperty(indexed=False, default=True)
    bucket = ferris.ndb.StringProperty(indexed=False, verbose_name="Leave blank to use the default GCS bucket.")


class OAuth2Setting(Setting):
    _name = 'OAuth2'
    _settings_key = 'oauth2'
    _description = """
    OAuth2 Configuration should be generated from
    <a href='https://code.google.com/apis/console'>The API Console</a>.
    """
    client_id = ferris.ndb.StringProperty(indexed=False)
    client_secret = ferris.ndb.StringProperty(indexed=False)
    developer_key = ferris.ndb.StringProperty(indexed=False)


class ServiceAccountSetting(Setting):
    _name = 'OAuth2 Service Account'
    _settings_key = 'oauth2_service_account'
    client_email = ferris.ndb.StringProperty(indexed=False, verbose_name="...@developer.gserviceaccount.com")
    private_key = ferris.ndb.TextProperty(verbose_name="PEM Format")
    developer_key = ferris.ndb.StringProperty(indexed=False)
