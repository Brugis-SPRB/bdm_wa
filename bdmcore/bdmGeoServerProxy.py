# -*- coding: utf-8 -*-


# # 
#  @file bdmGeoServerProxy.py
#  @brief Bdm Project | Web Access Subsystem | Wfs authorisation Proxy
#  @author Michel Van Asten
#  
from	rest_framework.views	import	APIView
from	rest_framework.response	import	Response	
import  requests

from    bdmcore.bdmCommandView import BdmCommandView
from    bdmcore.xmlPathThroughtRenderer import xmlPathThroughtRenderer
from 	workflow import settings


from	rest_framework	import	status
from	django.db	import	connection
from	collections	import	namedtuple
from    rest_framework_xml.parsers import XMLParser
from    rest_framework.parsers import JSONParser
from compiler.pycodegen import EXCEPT


# #
# WFS autorisation Proxy ... key is extracted from url (@see urls.py) 
class BdmWfsProxy(APIView):
	renderer_classes = (xmlPathThroughtRenderer,)
	parser_classes = (JSONParser, XMLParser,)
	_devSchema_admin	 = 	settings.DEVSCHEMA_ADMIN
	
	# #
	# Constructor
	# target Geoserver url, workspace and credentials are defined here
	def __init__(self):
		self._upstream = settings.WFS_UPSTREAM 
		
		self._user = settings.GEOSERVER_USER 
		self._pswd = settings.GEOSERVER_PWD
		self._workspace = settings.GEOSERVER_WORKSPACE
		
	
	def	get(self, 	request, 	*args, **kwargs):
		params	 = 	request.query_params
		userkey = kwargs['key']
		content = None
		return self.doProxy(request, params, userkey, content)
		
	def	post(self, 	request, 	*args, **kwargs):
		self.doDebugPrint("post 1")
		params	 = 	request.query_params
		try:
			content = request.body
		except Exception, e :
			self.doDebugPrint("post Exception")
			self.doDebugPrint(e)
		userkey = kwargs['key']
		return self.doProxy(request, params, userkey, content)
		
	# #
	# authorize user request ( token based) and forward request to upstream server
	# @param userkey user token
	# @param params query parameters 	
	# connection to upstream server performed with predefined credentials
	def	doProxy(self, 	request, params, userkey, content):
		self.doDebugPrint("doProxy 1")
		self.doDebugPrint(userkey)
		aut = self.wfs_authorize(request, userkey)
		hhtpstatus = status.HTTP_401_UNAUTHORIZED
		data = 'INVALID REQUEST'
		
		if aut:
			if (content is None):
				self.doDebugPrint("doProxy 3 1 get")
				resp = requests.get(self._upstream, params, auth=(self._user, self._pswd))
			else:
				self.doDebugPrint("doProxy 3 1 post")
				resp = None
				try:	
					resp = requests.post(self._upstream, content, auth=(self._user, self._pswd))
				except Exception, e :
					self.doDebugPrint("doProxy requests.post Exception")
					self.doDebugPrint(e)
			username = self.validateKey(userkey)
			BdmCommandView.s_lasterrors[username] = resp.text
			
			#data = resp.text
			try:
				c = resp.content
				data = c.decode('utf8')
			except Exception, e:
				self.doDebugPrint(  "cannot decode content" )
				data = ''
			
			# #
			# Check that content of valid response do not contain any Exception
			hhtpstatus = resp.status_code
			if resp.ok:
				if "ows:ExceptionReport" in data:
					self.doDebugPrint("Server Exception reported") 
					hhtpstatus = status.HTTP_500_INTERNAL_SERVER_ERROR
			else:
				self.doDebugPrint(  "doProxy RESP nok" )
			self.doDebugPrint(data)
		else:
			self.doDebugPrint( "doProxy authorisation failure")
			
		return	Response(data, 	status=hhtpstatus)
		
	
	
	# #
	# 
	# No access restriction on 'GETCAPABILITIES' and 'DESCRIBEFEATURETYPE' 
	# Access restriction on 'GETFEATURE'. Check 1° valid TOKEN 2° Bdm user right on layer (typename) 3° Bdm layer state (workflow) 	
	def wfs_authorize(self, request, userkey):
		# extract user
		username = self.validateKey(userkey)
		self.doDebugPrint( "username {}".format(username))
		wfsRequestType = "undefined"
		try:
			wfsRequestType = request.query_params['REQUEST'].upper()
		except Exception, e :
			wfsRequestType = "TRANSACTION"
			
		self.doDebugPrint(  "wfsRequestType {}".format(wfsRequestType))
		### Missing control on transaction
		if 'GETCAPABILITIES' == wfsRequestType or 'DESCRIBEFEATURETYPE' == wfsRequestType or 'TRANSACTION' == wfsRequestType:
			return True
		elif 'GETFEATURE' == wfsRequestType:
			# return True
			layername = request.query_params['TYPENAME']
			
			#tricky !!!! Remove table name prefix !!!!!
			cleanlayername = layername.replace("{}:".format(self._workspace), '')
			self.doDebugPrint( "cleanlayername {}".format(cleanlayername))
		
			state = self.getUserTableState(username, cleanlayername)
			# return len(state) > 0
			return True
		return True
	# #
	#
	# get userid if exist matching non expired key
	def validateKey(self, userkey):
		# return True
		querykey = "select user_name from {}.geokey where key = '{}' and  expiration > now()".format(self._devSchema_admin, userkey)
		res = self.dbQueryExecSingleton(querykey)
		return res

	# #
	# 	getUserTableState	:	get	table state	if the user	is owner of	the	last action
	def	getUserTableState(self, 	username, layername):
		statequery	 = 	"select	state	from	{}.tables_states where table_name =\'{}\'	and	user_name	=\'{}\'".format(self._devSchema_admin, layername, username)
		return self.dbQueryExec(statequery) 
		
	def	dbQueryExec(self, 	querystring):
		with	connection.cursor()	as	cursor:
			cursor.execute(querystring)
			results	 = 	self.namedtuplefetchall(cursor)
			if	len	(results) < 	1:
				return	''
			else:
				return results
	
	# #
	#
	# Return first element from a cursor
	def	dbQueryExecSingleton(self, 	querystring):
		with	connection.cursor()	as	cursor:
				cursor.execute(querystring)
				results	 = 	self.namedtuplefetchall(cursor)
				if	len	(results)	 < 	1:
					return	''
				else:
					return	results[0][0]
	
	# #
	#
	# Return	all	rows	from	a	cursor	as	a	namedtuple
	def	namedtuplefetchall(self, cursor):
		"Return	all	rows	from	a	cursor	as	a	namedtuple"
		desc	 = 	cursor.description
		nt_result	 = 	namedtuple('results', 	[col[0]	for	col	in	desc])
		return	[nt_result(*row)	for	row	in	cursor.fetchall()]	
	
	def doDebugPrint(self, debugmsg, severe=False):
		try:
			print debugmsg.decode('utf8')
		except:
			pass

# #
#
# Proxy d'autorisation pour les appels de configuration geoserver Rest... 
class BdmRestProxy(APIView):
	
	# #
	# Constructor
	# target url and credentials are defined here
	def __init__(self):
		self._upstream = settings.WFS_UPSTREAM 
		
		self._user = settings.GEOSERVER_USER 
		self._pswd = settings.GEOSERVER_PWD 
		self._workspace = settings.GEOSERVER_WORKSPACE
		
		
	def	get(self, 	request, 	format=None):
		params	 = 	request.query_params
		
		aut = self.wfs_authorize(request)
		hhtpstatus = status.HTTP_401_UNAUTHORIZED
		data = 'INVALID REQUEST'
		if aut:
			resp = requests.get(self._upstream, params, auth=(self._user, self._pswd))
			data = resp.text
			hhtpstatus = status.HTTP_200_OK
		return	Response(data, 	status=hhtpstatus)
		
		
	# #
	# TO DO...	
	def wfs_authorize(self, request):
		# to do
		uname = request.User.username
		return True
