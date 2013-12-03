from models import Plugin, Description, Rule, Cron
import json, git
from shutil import rmtree

try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH

def install(plugin_url=None, plugin_sha=None, plugin_name=None):
    try:
        if plugin_url and plugin_sha:
            repo = git.Repo.clone_from(plugin_url, LISA_PATH + '/Plugins/' + plugin_name)
            repo.git.checkout(plugin_sha)
        metadata = json.load(open(LISA_PATH + '/Plugins/' + plugin_name + '/' + str(plugin_name).lower() + '.json'))
        plugin = Plugin()
        description_list = []
        for item in metadata:
            if item != 'cron' or item != 'rules':
                if item == 'description':
                    for description in metadata[item]:
                        oDescription = Description()
                        for k,v in description.iteritems():
                            setattr(oDescription, k, v)
                        description_list.append(oDescription)
                    setattr(plugin, item, description_list)
                elif item == 'enabled':
                    if metadata[item] == 1:
                        setattr(plugin, item, True)
                    elif metadata[item] == 0:
                        setattr(plugin, item, False)
                    else:
                        setattr(plugin, item, True)
                else:
                    setattr(plugin, item, metadata[item])
        plugin.save()
        for item in metadata:
            if item == 'rules':
                for rule_item in metadata['rules']:
                    rule = Rule()
                    for parameter in rule_item:
                        setattr(rule, parameter, rule_item[parameter])
                    rule.plugin = plugin
                    rule.save()
            if item == 'crons':
                for cron_item in metadata['crons']:
                    cron = Cron()
                    for parameter in cron_item:
                        setattr(cron, parameter, cron_item[parameter])
                    cron.plugin = plugin
                    cron.save()
    except:
        return {'status': 'fail', 'log': 'There was a problem'}
    return {'status': 'success', 'log': 'Plugin Installed'}

"""
def enable(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            for plugin in Plugin.objects(pk=kwargs['pk']):
                plugin.enabled = True
                plugin.save()
                for cron in Cron.objects(plugin=plugin):
                    cron.enabled = True
                    cron.save()
        except:
            pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()
        return self.create_response(request, { 'status': 'success', 'log': "Plugin Enabled"}, HttpAccepted)

    def disable(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            for plugin in Plugin.objects(pk=kwargs['pk']):
                plugin.enabled = False
                plugin.save()
                for cron in Cron.objects(plugin=plugin):
                    cron.enabled = False
                    cron.save()
        except:
            pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()
        return self.create_response(request, { 'status': 'success', 'log': "Plugin Disabled"}, HttpAccepted)

    def uninstall(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            for plugin in Plugin.objects(pk=kwargs['pk']):
                rmtree(LISA_PATH + '/Plugins/' + plugin['name'])
                plugin.delete()
        except:
            pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()
        return self.create_response(request, { 'status': 'success', 'log': "Plugin Deleted"}, HttpAccepted)
"""