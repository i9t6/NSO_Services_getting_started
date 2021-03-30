# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

     # The create() callback is invoked inside NCS FASTMAP and
     # must always exist.
     @Service.create
     def cb_create(self, tctx, root, service, proplist):
         self.log.info('Service create(service=', service._path, ')')

         #..[setp stufff]....................................
         geoVars = ncs.template.Variables()
         template = ncs.template.Template(service)
         # initialize vars...
         geoVars.add('DEV', '')
         geoVars.add('COMMUNITY', '')
         geoVars.add('ACCESS', '')
         geoVars.add('DOMNAME', '')
         geoVars.add('DSRV', '')
         geoVars.add('NTP', '')
         #......

         #..[get the localTZ for the devices in this service instance]........
         #..[all devices in this service instance are in this TZ].............
         localTZ = service.localTZ
         self.log.debug('localTZ: ', localTZ)
         #..[now, read stuff from geo-catalog for this TZ]....................
         #..[dommain-name]..(leaf)..........................
         domName = root.GeoCatalog[localTZ].domainName
         self.log.debug('domName: ', domName)
         #..[nameServers]...(leaf-list).....................
         nameServers = root.GeoCatalog[localTZ].nameServer
         self.log.debug('num nameServers: ', len(nameServers))
         #..[ntpServers]...(leaf-list)......................
         ntpServers = root.GeoCatalog[localTZ].ntpServer
         self.log.debug('num ntpServers: ', len(ntpServers))
         #..[snmpRO][snmpRW]................................
         snmpRO = root.GeoCatalog[localTZ].snmpCommRO
         snmpRW = root.GeoCatalog[localTZ].snmpCommRW
         self.log.debug('snmpRO: ', snmpRO, ' snmpRW: ', snmpRW)
         #..
         #..ok, now we have everyone - let's write data out to devices........
         #..walk through all the devices (leaf-list)..........................
         for i, dev in enumerate(service.device):
             self.log.debug('dev: ', i, ' name: ', dev)
             geoVars.add('DEV', dev)
             geoVars.add('COMMUNITY', snmpRO)
             geoVars.add('ACCESS', 'ro')
             template.apply('geoPysnmp-template', geoVars)
             geoVars.add('COMMUNITY', snmpRW)
             geoVars.add('ACCESS', 'rw')
             template.apply('geoPysnmp-template', geoVars)
             geoVars.add('DOMNAME', domName)
             template.apply('geoPysnmp-template', geoVars)
             for dsrv in nameServers:
                 geoVars.add('DSRV', dsrv)
                 template.apply('geoPysnmp-template', geoVars)
             for ntp in ntpServers:
                 geoVars.add('NTP', ntp)
                 template.apply('geoPysnmp-template', geoVars)


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
     def setup(self):
         self.log.info('Main RUNNING')
         self.register_service('geoPysnmp-servicepoint', ServiceCallbacks)

     def teardown(self):
         self.log.info('Main FINISHED') 

