  # -*- coding: utf-8 -*-

# # 
#  @file bdmcommandview.py
#  @brief Bdm Project | Web Access Subsystem | Token management
#  @author Michel Van Asten
#  
from	rest_framework.views	import	APIView
from	rest_framework.response	import	Response
from	rest_framework	import	status
from	django.db	import	connection
import	smtplib
from	collections	import	namedtuple
import 	sys
import  uuid

from 	workflow import settings


# #
#
# Token generation and validation 
class	BdmKeyView(APIView):	
	def	__init__(self):
		self._devSchema_admin	 = 	settings.DEVSCHEMA_ADMIN
		self._jkeyFunction = 'functionvalue'	
	# #
	#
	# @param  request ( expected url parameters action [NEWKEY] and uname [USERNAME]
	def	get(self, 	request, 	format=None):
		action	 = 	request.query_params.get('action', 	None)
		res	 = 	'UNKNOWN ACTION'
		hhtpstatus = status.HTTP_400_BAD_REQUEST
		
		if	action	 == 	'NEWKEY':
			res	 = self.asJsonValue(self._jkeyFunction, self.getKey(request))	
			hhtpstatus = status.HTTP_200_OK
		elif	action	 == 	'VALIDATE':
			res	 = self.asJsonValue(self._jkeyFunction, self.validate(request))
			hhtpstatus = status.HTTP_200_OK
		return	Response(res, 	status=hhtpstatus)
	
	# #
	#
	# @param  request ( expected query parameters action [NEWKEY] and uname [USERNAME]
	def	post(self, 	request, 	format=None):
		action	 = 	request.query_params.get('action', 	None)
		res	 = 	'UNKNOWN ACTION'
		hhtpstatus = status.HTTP_400_BAD_REQUEST
		
		if	action	 == 	'NEWKEY':
			res	 = self.asJsonValue(self._jkeyFunction, self.getKey(request))	
			hhtpstatus = status.HTTP_200_OK
		elif	action	 == 	'VALIDATE':
			res	 = self.asJsonValue(self._jkeyFunction, self.validate(request))
			hhtpstatus = status.HTTP_200_OK
		return	Response(res, 	status=hhtpstatus)
	
	# #
	# Generate and persist new key (TOKEN)
	# @param  request (expected query parameters [USERNAME]
	def getKey(self, request):
		usr	 = request.query_params.get('uname', 	None)
		newUID = uuid.uuid4()
		querydelete = "delete from {}.geokey where user_name = '{}'".format(self._devSchema_admin, usr)
		queryinsert = "insert into {}.geokey (user_name,key) values('{}','{}')".format(self._devSchema_admin, usr, newUID)
		self.dbRawExec(querydelete)
		self.dbRawExec(queryinsert)
		return newUID
	
	def validate(self, request):
		key	 = request.query_params.get('key', 	None)
		queryexist = "select user_name from {}.geokey key = '{}' and where expiration > now()".format(self._devSchema_admin, key)
		return self.dbQueryExecSingleton(queryexist)
	
	
	
	def	dbRawExec(self, querystring):
		with	connection.cursor()	as	cursor:
				cursor.execute('SET search_path TO public')
				cursor.execute(querystring)
	
	def	dbQueryExecSingleton(self, 	querystring):
		with	connection.cursor()	as	cursor:
				cursor.execute('SET search_path TO public')
				cursor.execute(querystring)
				results	 = 	self.namedtuplefetchall(cursor)
				if	len	(results)	 < 	1:
					return	''
				else:
					return	results[0][0]
	
	def	asJsonValue(self, name, 	value):
		d	 = 	{name:	value}
		return	d
		



# #
#
# Bdm command implementation
class	BdmCommandView(APIView):
	s_lasterrors = dict()	
	def	__init__(self):
		self._adminuser			 = 	settings.ADMIN_USER	
		self._devSchema_edit	 = 	settings.DEVSCHEMA_EDIT	
		self._devSchema_modif	 = 	settings.DEVSCHEMA_MODIF
		self._devSchema_intra	 = 	settings.DEVSCHEMA_INTRA
		self._devSchema_admin	 = 	settings.DEVSCHEMA_ADMIN
		self._devSchema_common	 = 	settings.DEVSCHEMA_COMMON
		self._devSchema_publish = 	settings.DEVSCHEMA_PUBLISH
		
		self._brugis_dataflow_cout	 = 	settings.BRUGIS_DATAFLOW_COUT	
		self._brugis_dataflow_cin	 = 	settings.BRUGIS_DATAFLOW_CIN	
		self._brugis_dataflow_staging	 = 	settings.BRUGIS_DATAFLOW_STAGING	
		self._brugis_dataflow_valid	 = 	settings.BRUGIS_DATAFLOW_VALID
		self._brugis_dataflow_undefined	 = 	settings.BRUGIS_DATAFLOW_UNDEFINED

		self._brugis_useraction_CHECKOUT	 = 	settings.BRUGIS_USERACTION_CHECKOUT
		self._brugis_useraction_VALIDATE	 = 	settings.BRUGIS_USERACTION_VALIDATE
		self._brugis_useraction_STAGING		 = 	settings.BRUGIS_USERACTION_STAGING
		self._brugis_useraction_UNDOCHECKOUT	 = 	settings.BRUGIS_USERACTION_UNDOCHECKOUT
		self._brugis_useraction_UNDOSTAGING	 = 	settings.BRUGIS_USERACTION_UNDOSTAGING
			
		
		self._brugisEmailAdress	 = 	settings.BRUGIS_MAIL_ADDR
		self._emailDefaultSubject	 = 	settings.BRUGIS_MAIL_SUBJECT
		self._brugisSmtp			 = 	settings.BRUGIS_MAIL_SMTP
		self._myVersion				 = 	settings.BDM_VERSION	
		self._jkeyFunction = 'functionvalue'	
	

		
		
	def validate(self, request):
		key	 = request.query_params.get('key', 	None)
		print request.query_params
		queryexist = "select user_name from {}.geokey where key = '{}' and expiration > now()".format(self._devSchema_admin, key)
		print queryexist
		usr = self.dbQueryExecSingleton(queryexist)
		if len(usr) < 1:
			return "undefined"
		else:
			return usr
	
	def	get(self, 	request, 	format=None):
		action	 = 	request.query_params.get('action', 	None)
		uname = self.validate(request)
		
		print "--E EXEC {} for {}".format(action, uname) 
	
		
		res	 = 	'UNKNOWN ACTION'
		hhtpstatus = status.HTTP_200_OK
		
		if	action	 == 	'GEOTYPE':
			res	 = 	self.doGetGeometryType(uname, request)
		elif	action	 == 	'PKDEFAULT':
			res	 = 	self.doPkDefaultValue(uname, request)	
		elif	action	 == 	'COPY_ME':
			res	 = 	self.doCopyTableModifToEdit(uname, request)	
		elif	action	 == 	'COPY_EM':
			res	 = 	self.doCopyTableEditToModif(uname, request)	
		elif	action	 == 	'COPY_IE':
			res	 = 	self.doCopyTableIntraToEdit(uname, request)
		elif	action	 == 	'SAFE_COPY_MI':
			res	 = 	self.doSafeCopyTableModifIntra(uname, request)
		elif	action	 == 	'SAFE_COPY_PU':	
			res	 = 	self.doSafeCopyTableModifPublish(uname, request)
		elif	action	 == 	'ASSIGN_DEFAULT':
			res	 = 	self.doTableDefaultAssign(uname, request)
		elif	action	 == 	'E_DROP':
			res	 = 	self.tableEditDrop(uname, request)
		elif	action	 == 	'IS_EDIT_GRANTED':	
			res = self.isUserEditGranted()
		elif	action	 == 	'M_DROP':
			res	 = 	self.tableModifDrop(uname, request)
		elif	action	 == 	'SEND_MAIL':
			res	 = 	self.doSendMail(uname, request)
		elif	action	 == 	'KEEPALIVE':
			res	 = 	'Ceci est un test secret'
			hhtpstatus = status.HTTP_200_OK
		elif	action	 == 	'GRANT':
			self.doGrantEdit(uname, request)
			res	 = 	'DONE'
		elif	action	 == 	'REVOKE':
			self.doRevokeEdit(uname, request)
			res	 = 	'DONE'
		elif	action	 == 	'EVENT':
			self.doBrugisEvent(uname, request)
			res	 = 	'DONE'
		elif	action	 == 	'R_C_STATUS':
			self.resetCreationStatus(uname, request)
			res	 = 	'DONE'
		elif	action	 == 	'U_LOCK':
			res	 = self.getUserLock(uname, request)	
		elif	action	 == 	'CLEANUP_ORPHANED':
			res = self.doCleanupOrphaned(uname, request)		
		elif	action	 == 	'U_T_STATE':
			res	 = 	self.getUserTableState(uname, request)
		elif	action	 == 	'U_A_STATE':
			res	 = 	self.getUserActivityState(uname, request)
		elif	action	 == 	'T_S_STATE':
			res	 = 	self.getTableState(uname, request)	
		elif	action	 == 	'T_S_STATECREA':
			res	 = 	self.getTableStateCrea(uname, request)
		elif	action	 == 	'T_L_OWNER':
			res	 = 	self.getTableLastOwner(uname, request)
		elif	action	 == 	'T_ASSIGNED':
			res	 = 	self.isTableAssigned(uname, request)
		elif	action	 == 	'U_L_STATUS':
			res	 = 	self.updateLayerStatus(uname, request)
		elif	action	 == 	'C_CHECK':
			res	 = 	self.doCheckConsistency(uname, request)
		elif	action	 == 	'IS_VALID':
			res	 = 	self.getGeometryValid(uname, request)
		elif	action	 == 	'L_U_SESSION':
			res	 = 	self.doLockUserSession(uname, request)
		elif	action	 == 	'U_U_SESSION':
			res	 = 	self.doUnLockUserSession(uname, request)
		elif	action	 == 	'GET_G_LOCK':			
			res = self.doCheckGlobalLock()
		elif	action	 == 	'LAST_ERROR':	
			res	 = 	self.getLastError(uname, request)	
		elif 	action	 == 	'ALL_USERTABLES':
			res	 = 	self.getAllUserTables(uname, request)
		else:
			hhtpstatus = status.HTTP_400_BAD_REQUEST
		
		
		
			
			
		return	Response(res, 	status=hhtpstatus)
	
	def getLastError(self, uname, request):
		print "check last error for {}".format(uname)
		if uname in BdmCommandView.s_lasterrors:
			print BdmCommandView.s_lasterrors[uname]
			return	self.asJsonValue(self._jkeyFunction, BdmCommandView.s_lasterrors[uname])	
		
	
	def	getUserLock(self, uname, request):
		usrname	 = 	uname
		querystring	 = 	"SELECT	slock	from	{}.users	where	username=\'{}\'	".format(self._devSchema_admin, usrname)
		val	 = 	self.dbQueryExecSingleton(querystring)
		return	self.asJsonValue(self._jkeyFunction, val)
		
	
	def	getAllUserTables(self, 	uname, request):
		username	 = 	request.query_params.get('uname', 	None)
		querystring	 = 	"select table_name from {}.user_rights where user_name = \'{}\' order by table_name ;".format(self._devSchema_admin, username)
		val	 = 	self.dbQueryExec(querystring)
		return	self.asJsonValue(self._jkeyFunction, val)
	
		
	
	def	doGetGeometryType(self, 	uname, request):
		tbl	 = 	request.query_params.get('lname', 	None)		
		querystring	 = 	"select	commonbrugis.getgeometrytype(\'brugis_edittmp\',\'{}\')".format(tbl)
		self.dbRawExec(querystring)
		
	def	doTableDefaultAssign(self, 	uname, request):
		tbl	 = 	request.query_params.get('lname', 	None)		
		querystring	 = 	"insert	into	{}.user_rights	(	table_name,	schema_name,	user_name	)	values	(\'{}\',\'brugis_intra\',\'{}\')".format(self._devSchema_admin, tbl, self._adminuser)	
		self.dbRawExec(querystring)
		querystring	 = 	"insert	into	{}.tables_states	(schema_name,	state,	statecrea,	user_name,	table_name)	values	(\'brugis_intra\',\'COUT\',\'NEW\',\'{}\',\'{}\')".format(self._devSchema_admin, self._adminuser, 	tbl)
		self.dbRawExec(querystring)	
		
	
	def	doLockUserSession(self, uname, request):
		usrname	 = 	uname
		querystring	 = 	"update	{}.users	set	slock	=	1	where	username=\'{}\'".format(self._devSchema_admin, usrname)
		self.dbRawExec(querystring)
		
	def doCleanupOrphaned(self, uname, request):
		querystring = "select commonbrugis.cleanup_orphaned()"
		self.dbRawExec(querystring)

		
	def doCheckGlobalLock(self):
		lockquery = "select value from {}.globalparams where name = \'globallock\' and value = \'TRUE\'".format(self._devSchema_admin)
		val = self.dbQueryExecSingleton(lockquery)
		return	self.asJsonValue(self._jkeyFunction, val)
	
	def	doUnLockUserSession(self, uname, request):
		usrname	 = 	uname
		querystring	 = 	"update	{}.users	set	slock	=	0	where	username=\'{}\'".format(self._devSchema_admin, usrname)
		self.dbRawExec(querystring)	
	
	
	def	doPkDefaultValue(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		query_toserial	 = 	"select	commonbrugis.change_integer_pk_to_serial	(\'{}\',	\'{}\')".format(layername, 	self._devSchema_edit)
		query_setdefault	 = 	"select	commonbrugis.change_pk_use_sequence(\'{}\',	\'{}\')".format(layername, 	self._devSchema_edit)
		self.dbRawExec(query_toserial)
		self.dbRawExec(query_setdefault)
	
	
	def	doCopyTableModifToEdit(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		therequest	 = 	"select	commonbrugis.copy_table(\'{}\',	\'{}\',	\'{}')".format(self._devSchema_modif, self._devSchema_edit, layername)
		self.dbRawExec(therequest)
		therequestConst	 = 	"select	commonbrugis.copy_std_constraints(\'{}\',	\'{}\',	\'{}\')".format(self._devSchema_modif, self._devSchema_edit, layername)
		self.dbRawExec(therequestConst)	
		therequest	 = 	"select	commonbrugis.change_pk_use_sequence(\'{}\',	\'{}\')".format(layername, self._devSchema_edit)
		self.dbRawExec(therequestConst)
		droprequest	 = 	"drop	table	\"{}\".\"{}\"".format(self._devSchema_modif, layername)
		self.dbRawExec(droprequest)	
		
	def	tableEditDrop(self, uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		therequest	 = 	"drop	table	\"{}\".\"{}\"".format(self._devSchema_edit, layername)
		self.dbRawExec(therequest)
		
	
	def	doCopyTableEditToModif(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		therequest	 = 	"select	commonbrugis.copy_table(\'{}\',	\'{}\',	\'{}')".format(self._devSchema_edit, self._devSchema_modif, layername)
		self.dbRawExec(therequest)		
		therequestConst	 = 	"select	commonbrugis.copy_std_constraints(\'{}\',	\'{}\',	\'{}\')".format(self._devSchema_edit, self._devSchema_modif, layername)
		self.dbRawExec(therequestConst)
		droprequest	 = 	"drop	table	\"{}\".\"{}\"".format(self._devSchema_edit, layername)
		self.dbRawExec(droprequest)
			
	
	def	doCopyTableIntraToEdit(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		therequest	 = 	"select	commonbrugis.copy_table(\'{}\',	\'{}\',	\'{}')".format(self._devSchema_intra, self._devSchema_edit, layername)
		self.dbRawExec(therequest)
		therequestConst	 = 	"select	commonbrugis.copy_std_constraints(\'{}\',	\'{}\',	\'{}\')".format(self._devSchema_intra, self._devSchema_edit, layername)
		self.dbRawExec(therequestConst)
		
	def	doSafeCopyTableModifIntra(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		therequest	 = 	"select	commonbrugis.safe_copy_table(\'{}\',	\'{}\',	\'{}\')".format(self._devSchema_modif, 	self._devSchema_intra, 	layername)
		self.dbRawExec(therequest)
		therequestConst	 = 	"select	commonbrugis.copy_std_constraints(\'{}\',	\'{}\',	\'{}\')".format(self._devSchema_modif, 	self._devSchema_intra, layername)
		self.dbRawExec(therequestConst)	
	
	def	doSafeCopyTableModifPublish(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		therequest	 = 	"select	commonbrugis.safe_copy_table(\'{}\',	\'{}\',	\'{}\')".format(self._devSchema_modif, 	self._devSchema_publish, 	layername)
		self.dbRawExec(therequest)
		therequestConst	 = 	"select	commonbrugis.copy_std_constraints(\'{}\',	\'{}\',	\'{}\')".format(self._devSchema_modif, 	self._devSchema_publish, layername)
		self.dbRawExec(therequestConst)	
	
	
	def	removeLayerStatus(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		insertrequest	 = 	"delete	from	{}.tables_states	where	table_name	=	\'{}\')".format(self._devSchema_admin, layername)
		self.dbRawExec(insertrequest)
	
		
	def	resetCreationStatus(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		updaterequest	 = 	"update	{}.tables_states	set	statecrea	=	null	where	table_name	=	\'{}\'".format(self._devSchema_admin, layername)
		self.dbRawExec(updaterequest)
		
	def	updateLayerStatus(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		usrname	 = 	uname
		status	 = 	request.query_params.get('status', 	None)	
		print "updateLayerStatus {} {} {}".format(usrname,status,layername)	
		if	usrname == "undefined":	
			insertrequest	 = 	"insert	into	{}.tables_states	(schema_name,	state,	user_name,	table_name)	values	(\'brugis_intra\',\'{}\',\'{}\',	\'{}\')".format(self._devSchema_admin, status, self._adminuser, 	layername)
			updaterequest	 = 	"update	{}.tables_states	set	state	=	\'{}\'	where	table_name	=	\'{}\'".format(self._devSchema_admin, status, layername)
									
		else:
			insertrequest	 = 	"insert	into	{}.tables_states	(schema_name,	state,	user_name,	table_name)	values	(\'brugis_intra\',\'{}\',\'{}\',	\'{}\')".format(self._devSchema_admin, status, usrname, 	layername)
			updaterequest	 = 	"update	{}.tables_states	set	state	=	\'{}\',	user_name	=	\'{}\'	where	table_name	=	\'{}\'".format(self._devSchema_admin, status, usrname, layername)			
		try:
			self.dbRawExec(insertrequest)
		except:
			self.dbRawExec(updaterequest)
			pass
	
	def isUserEditGranted(self):
		grantedrequest = "select commonbrugis.isbrugiseditorgrantee()"
		val	 = 	self.dbQueryExecSingleton(grantedrequest)
		return	self.asJsonValue(self._jkeyFunction, val)

	def	doCheckConsistency(self, uname, request):
		username	 = 	uname
		consitencyquery	 = 	"select	table_name	from	{}.tables_states	where	user_name	=	\'{}\'	and	state	<>	'CIN'	AND	table_name	not	in	(select	tablename	from	pg_tables	where	schemaname	=	'brugis_edittmp'	OR	schemaname	=	'brugis_modif'	)".format(self._devSchema_admin, username)
		val	 = 	self.dbQueryExec(consitencyquery)
		return	self.asJsonValue(self._jkeyFunction, val)

	def	getUserMail(self, 	uname, request):
		username	 = 	uname
		self.doDebugPrint("getUserMail	"	 + 	username)
		therequest	 = 	"SELECT	usermail	from	{}.users	where	username=\'{}\'	".format(self._devSchema_admin, username)
		val	 = 	self.dbQueryExecSingleton(therequest)
		return	self.asJsonValue(self._jkeyFunction, val)
		
		
	# #
	# 	getUserTableState	:	get	table	state	is	the	user	is	owner	of	the	last	action
	#
	def	getUserTableState(self, 	uname, request):
		username	 = 	request.query_params.get('uname', 	None)
		if username is None:
			username = uname
		layername	 = 	request.query_params.get('lname', 	None)
		statequery	 = 	"select	state	from	{}.tables_states where table_name =\'{}\'	and	user_name	=\'{}\'".format(self._devSchema_admin, layername, username)
		val	 = 	self.dbQueryExecSingleton(statequery)
		if val == None:
			val = self._brugis_dataflow_undefined
		elif len(val) == 0:
			val = self._brugis_dataflow_undefined
			
		
		return	self.asJsonValue(self._jkeyFunction, val)

	# #
	# 	getUserActivityState	:	Check if exist any	table	"owned	by	this	user",	returns	the	state
	#
	def	getUserActivityState(self, 	uname, request):
		username	 = 	request.query_params.get('uname', 	None)
		# layername	=	request.query_params.get('lname',	None)
	
		statequery	 = 	"select	state	from	{}.tables_states	where	user_name	=\'{}\'	and	state	<>	\'{}\'".format(self._devSchema_admin, username, 	self._brugis_dataflow_cin)
		val	 = 	self.dbQueryExec(statequery)
		if	len(val)	 < 	1	:
			val	 = 	self._brugis_dataflow_cin
		return	self.asJsonValue(self._jkeyFunction, val)
		
			
	# #
	# 	getTableState	:	retrieve	current	layer	state	in	brugis_admin.tables_states
	#
	def	getTableState(self, 	uname, request):	
		layername	 = 	request.query_params.get('lname', 	None)
		statequery	 = 	"select	state	from	{}.tables_states	where	table_name	=\'{}\'".format(self._devSchema_admin, layername)
		val	 = 	self.dbQueryExecSingleton(statequery)
		if	val	is	None:
			val	 = 	self._brugis_dataflow_cin
		elif len(val) < 	1:
			val	 = 	self._brugis_dataflow_cin
		print "getTableState {} {}".format(layername, val)
		return	self.asJsonValue(self._jkeyFunction, val)
		
			
	# #
	# 	getTableStateCrea	:	retrieve	creation	status	of	current	layer	state	in	brugis_admin.tables_states
	#
	def	getTableStateCrea(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		statequery	 = 	"select	statecrea	from	{}.tables_states	where	table_name	=\'{}\'".format(self._devSchema_admin, layername)
		val	 = 	self.dbQueryExecSingleton(statequery)
		return	self.asJsonValue(self._jkeyFunction, val)
	
	# #
	# 	getTableLastOwner	:	retrieve	last	action	owner	(user_name)	for	this	table
	#
	def	getTableLastOwner(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		statequery	 = 	"select	user_name	from	{}.tables_states	where	table_name	=\'{}\'".format(self._devSchema_admin, layername)
		val	 = 	self.dbQueryExecSingleton(statequery)
		return	self.asJsonValue(self._jkeyFunction, val)
		
	# #
	# 	isTableAssigned	:	check	if	table	is	assigned	to	any	user
	#
	def	isTableAssigned(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		statequery	 = 	"select	user_name	from	{}.user_rights	where	table_name	=\'{}\'".format(self._devSchema_admin, layername)
		val	 = 	self.dbQueryExist(statequery)
		return	self.asJsonValue(self._jkeyFunction, val)
		
	
	def	doGrantEdit(self, 	uname, request):
		# restore	grant	on	schema	editemp
		grantusage	 = 	"GRANT	USAGE	ON	SCHEMA	brugis_edittmp	TO	brugis_editor"
		self.dbRawExec(grantusage)
		grant	 = 	"GRANT	SELECT,	UPDATE,	DELETE,	INSERT	ON	ALL	TABLES	IN	SCHEMA	brugis_edittmp	TO	brugis_editor"
		self.dbRawExec(grant)
		
		grant_sequence	 = 	"GRANT	USAGE,	SELECT,	UPDATE	ON	ALL	SEQUENCES	IN	SCHEMA	brugis_edittmp	TO	brugis_editor	;"
		self.dbRawExec(grant_sequence)
		
	def	doRevokeEdit(self, 	uname, request):
		# restore	grant	on	schema	editemp
		grant_revoke	 = 	"REVOKE	SELECT,	UPDATE,	DELETE,	INSERT	ON	ALL	TABLES	IN	SCHEMA	brugis_edittmp	FROM	brugis_editor"
		take_ownership	 = 	"select	commonbrugis.transfer_all_checkout(\'{}\')".format(self._adminuser)
		self.dbRawExec(grant_revoke)
		self.dbRawExec(take_ownership)
		
		
	def	doSendMail(self, 	uname, request):
		params	 = 	request.query_params
		body	 = 	params.get('mail_message', 	None)
		receiver	 = 	params.get('mail_recipient', 	None)
		subject	 = 	self._emailDefaultSubject
		
		sender	 = 	self._brugisEmailAdress
		msg	 = 	"\r\n".join(["From:	"	 + 	sender, 	"To:	"	 + 	receiver, "Subject:	"	 + 	subject, "", 	body])
		try:
			server	 = 	smtplib.SMTP(self._brugisSmtp)
			server.ehlo()
			server.sendmail(sender, 	receiver, 	msg)
			self.doNotify('sendmail	succeed')
		except	Exception	:
			self.doNotify('Error: Unable to	send email {}'.format(sys.exc_info()[0]))
	
	def	getGeometryValid(self, uname, request):
		params	 = 	request.query_params
		layername	 = 	params.get('lname', 	None)
		queryStructure	 = 	"select	\"ID\",	\"GEOMETRY\"	from	\"{}\".\"{}\"".format(self._devSchema_edit, layername)	
		val	 = 	self.dbQueryExec(queryStructure)
		if	len(val)	 < 	1:
			val	 = 	"Invalid table structure"
		else:
			queryErrDisplay	 = 	"select	ST_IsValidReason(\"GEOMETRY\")	R	from	\"{}\".\"{}\"	where	not	ST_ISVALID(\"GEOMETRY\")".format(self._devSchema_edit, layername)
			val	 = 	self.dbQueryExec(queryErrDisplay)
		return	self.asJsonValue('VALID', val)

	def	doBrugisEvent(self, 	uname, request):
		params	 = 	request.query_params
		lname	 = 	params.get('layername', 	None)
		baction	 = 	params.get('trans', 	None)
		state	 = 	params.get('state', 	None)
		res	 = 	params.get('result', 	None)	
		info	 = 	params.get('info', 	None)
		context	 = 	"BdmWebAccess"
		hname	 = 	request.META['REMOTE_ADDR']
		print request.META
		eventQuery	 = 	"""insert	into	{}.events(
		user_name,	table_name,	action,	initialstate,	context,	result,	
		info,	client)	VALUES	('{}',	'{}',	'{}',	'{}',	'{}',	'{}',	'{}',	'{}')""".format(self._devSchema_admin, uname, 	lname, baction, state, context	 + 	"_"	 + 	self._myVersion, res, info, hname)
		self.dbRawExec(eventQuery)
	
	#####################################
	# 	Utility methods
	def	dbRawExec(self, querystring):
		with	connection.cursor()	as	cursor:
				cursor.execute('SET search_path TO public')
				cursor.execute(querystring)
	
	def	dbQueryExecSingleton(self, 	querystring):
		with	connection.cursor()	as	cursor:
				cursor.execute('SET search_path TO public')
				cursor.execute(querystring)
				results	 = 	self.namedtuplefetchall(cursor)
				if	len	(results)	 < 	1:
					return	''
				else:
					return	results[0][0]
	
	
	
	def	dbQueryExec(self, 	querystring):
		with	connection.cursor()	as	cursor:
				cursor.execute('SET search_path TO public')
				cursor.execute(querystring)
				results	 = 	self.namedtuplefetchall(cursor)
				if	len	(results)	 < 	1:
					return	''
				else:
					return	results
	
	def	dbQueryExist(self, 	querystring):
		try:
			with	connection.cursor()	as	cursor:
				cursor.execute(querystring)
				results	 = 	self.namedtuplefetchall(cursor)
				if	len	(results)	 < 	1:
					return	'False'
				else:
					return	'True'
		except	Exception	:
			return	'False'
		
		
	def	namedtuplefetchall(self, cursor):
		"Return	all	rows	from	a	cursor	as	a	namedtuple"
		desc	 = 	cursor.description
		nt_result	 = 	namedtuple('results', 	[col[0]	for	col	in	desc])
		return	[nt_result(*row)	for	row	in	cursor.fetchall()]	
	
	def	asJsonValue(self, name, 	value):
		d	 = 	{name:	value}
		return	d
	
	
