import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')  # Default value


class EnvironMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'DJANGO_SETTINGS_MODULE' in environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = environ['DJANGO_SETTINGS_MODULE']
        return self.app(environ, start_response)


# class NewRelicWrapper(object):
#     def __init__(self, app):
#         self.app = app

#     def __call__(self, environ, start_response):
#         new_relic_env = os.environ['DJANGO_SETTINGS_MODULE'].rsplit('.', 1)[-1] or None

#         newrelic.agent.initialize(os.path.join(PROJECT_PATH, 'newrelic.ini'), new_relic_env)
#         return newrelic.agent.WSGIApplicationWrapper(self.app)(environ, start_response)


# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = EnvironMiddleware(get_wsgi_application())
