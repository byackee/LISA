from django.conf.urls import patterns, include, url
from tastypie.api import Api
from plugins.api import PluginResource
from api import LisaResource
from twisted.python.reflect import namedAny
import tastypie_swagger

v1_api = Api(api_name='v1')
v1_api.register(PluginResource())
v1_api.register(LisaResource())

from libs.Server import enabled_plugins
for plugin in enabled_plugins:
    metapluginResource = namedAny(plugin+'.web.api.'+plugin+'Resource')
    v1_api.register(metapluginResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/docs/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    url(r'^speech/', include('googlespeech.urls')),
    url(r'^plugins/', include('plugins.urls')),
    url(r'', include('interface.urls')),
)
