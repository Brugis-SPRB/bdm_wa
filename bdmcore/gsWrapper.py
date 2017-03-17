# -*- coding: utf-8 -*-

# # 
# @file gsWrapper.py
# @brief Bdm Project | Web Access Subsystem | Geoserver administration
# @author Michel Van Asten

from geoserver.catalog import Catalog
from geoserver.resource import FeatureType

from workflow import settings


# #  
# Geoserver administration (wrapper)
# basé sur impl�mentation python "gsconfig" de geoserver
class gsWrapper(object):

	# #
	# Constructor
	# target Geoserver url, workspace, store and credentials are defined here
	def __init__(self): 
		self._upstream = settings.WFS_UPSTREAM 
		
		self._user = settings.GEOSERVER_USER 
		self._pswd = settings.GEOSERVER_PWD
		self._workspace = settings.GEOSERVER_WORKSPACE
		
		self._geoserverurl = settings.GEOSERVER_REST
		self._datastore = settings.GEOSERVER_DATASTORE
		
		self._geometryField = settings.GEOMETRYFIELD
		self._srid = settings.DEFAULTSRID
		self._headers = settings.WFS_HEADERS
		
	# #
	# Return Catalog using prefefined credentials	
	def getCatalog(self):
		return Catalog(self._geoserverurl, self._user, self._pswd)

	# #
	# Return true if layer name already exist on strore
	# @param lname layername( with workspace prefix)		
	def existLayer(self, lname):
		cat = self.getCatalog()
		
		c_la = cat.get_layer(lname)
		return (c_la != None)

	# #
	# Add a new layer to the workspace
	# @note: if layer already exist do nothing
	# @param lname layername( without workspace prefix)	
	# @param geometrytype layer geometry type ( as retrieved via PostGis )	
	def addLayer(self, lname, geometrytype):
		fullname = "{}:{}".format(self._workspace, lname)
		cat = self.getCatalog()
		store = cat.get_store(self._datastore)
		print "fullname is {}".format(fullname)
		print "store is {}".format(store)  
		c_la = cat.get_layer(fullname)
		if c_la != None:
			print "layer {} already exist".format(fullname)
			return False
		
		listmetadata = dict()
		listmetadata['cachingEnabled'] = 'false' 
		
		feature_type = FeatureType(cat, store.workspace, store, fullname)
		# because name is the in FeatureType base class, work around that
		# and hack in these others that don't have xml properties
		feature_type.dirty['name'] = lname
		feature_type.dirty['srs'] = self._srid 
		feature_type.dirty['nativeCRS'] = self._srid
		feature_type.enabled = True
		feature_type.title = lname
		feature_type.native_name = lname
		feature_type.metadata = listmetadata
		
		print "message {}".format(feature_type.message())
		headers, response = cat.http.request(store.resource_url, "POST", feature_type.message(), self._headers)
		
		print "response {}".format(response)
		
		return True

	# #
	# remove layer from the workspace
	# @param lname layername( without workspace prefix) 	
	def removeLayer(self, lname):
		fullname = "{}:{}".format(self._workspace, lname)
		print "removeLayer"
		print "fullname is {}".format(fullname)
		
		cat = self.getCatalog()
		
		c_la = cat.get_layer(fullname)
		cat.delete(c_la)
		cat.reload()

		return True
	
