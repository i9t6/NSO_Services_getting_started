# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        snmpVars = ncs.template.Variables()
        snmpVars.add('COMMUNITY', "python-demo" + service.comm_str)
        snmpVars.add('ACCESS', service.access)
        
        template = ncs.template.Template(service)
        template.apply('snmpPyTemp5-template', snmpVars)
        self.log.info('snmpPyTemp5: comm: ', service.comm_str, ' access: ', service.access)


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_service('snmpPyTemp5-servicepoint', ServiceCallbacks)

    def teardown(self):
        self.log.info('Main FINISHED')
