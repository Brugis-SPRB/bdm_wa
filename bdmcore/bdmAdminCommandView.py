  # -*- coding: utf-8 -*-

# # 
#  @file bdmAdminCommandView.py
#  @brief Bdm Project | Web Access Subsystem | Pluggin Web API (administration command)
#  @author Michel Van Asten
#  
from	rest_framework.views	import	APIView
from	rest_framework.response	import	Response
from	rest_framework	import	status
from	django.db	import	connection
from	django.contrib.auth.models	import	User
from	collections	import	namedtuple
from    gsWrapper import gsWrapper
from    workflow import settings


# #
#
# Administration command implementation
class	BdmAdminCommandView(APIView):	
	def	__init__(self):
		self._adminuser			 = 	settings.ADMIN_USER
		self._devSchema_edit	 = 	settings.DEVSCHEMA_EDIT	
		self._devSchema_modif	 = 	settings.DEVSCHEMA_MODIF
		self._devSchema_intra	 = 	settings.DEVSCHEMA_INTRA
		self._devSchema_admin	 = 	settings.DEVSCHEMA_ADMIN
		self._devSchema_common	 = 	settings.DEVSCHEMA_COMMON
		
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
		self._brugisSmtp	 = 	settings.BRUGIS_MAIL_SMTP
		self._myVersion	 = 	settings.BDM_VERSION
		self._jkeyFunction = 'functionvalue'
		
	def validate(self, request):
		key	 = request.query_params.get('key', 	None)
		queryexist = "select user_name from brugis_qgisplugin_admin.geokey where key = '{}' and expiration > now()".format(key)
		usr = self.dbQueryExecSingleton(queryexist)
		if len(usr) < 1:
			return "undefined"
		else:
			return usr
	
	def	get(self, 	request, 	format=None):
		action	 = 	request.query_params.get('action', 	None)
		uname = self.validate(request)
		
		print "--E EXEC {} for {}".format(action, uname) 
		
		res	 = 	'UNKNOWN	ACTION'
		hhtpstatus = status.HTTP_200_OK
		
		if	action	 == 	'TRANSFCOUT':
			res	 = 	self.doTransfertAllCheckout(uname, request)	
		elif	action	 == 	'ASSIGN_LAYER':
			res	 = 	self.doAssignLayer(uname, request)
		elif	action	 == 	'DEFAULT_ASSIGN':
			res	 = 	self.doTableDefaultAssign(uname, request)
		elif	action	 == 	'IMPORT_VALIDATE':
			res	 = 	self.doValidateImport(uname, request)
		elif	action	 == 	'ADD_GS_LAYER':
			res	 = 	self.addGSLayer(uname, request)
		elif	action	 == 	'REMOVE_GS_LAYER':
			res	 = 	self.removeGSLayer(uname, request)
		elif	action	 == 	'REMOVE_RIGHT':
			res	 = 	self.removeUserRight(uname, request)
		elif	action	 == 	'REMOVE_ALL_RIGHT':	
			res	 = 	self.removeUserRightOnAllLayer(uname, request)
		elif	action	 == 	'DO_PK':	
			res	 = 	self.doPk(uname, request)
		elif	action	 == 	'E_DROP':
			res	 = 	self.tableEditDrop(uname, request)
		elif	action	 == 	'GRANT':
			self.doGrantEdit(uname, request)
			res	 = 	'DONE'
		elif	action	 == 	'REVOKE':
			self.doRevokeEdit(uname, request)
			res	 = 	'DONE'
		elif	action	 == 	'DELETE_USER':
			self.doDeleteUser(uname, request)
			res	 = 	'DONE'
		elif	action	 == 	'CREATE_USER':
			self.createUser(uname, request)
			res	 = 	'DONE'
		elif	action	 == 	'UPDATE_USER':
			self.updateUser(uname, request)
			res	 = 	'DONE'
		elif	action	 == 	'RESET_G_LOCK':
			res	 = self.resetGlobalLock(uname, request)	
		elif	action	 == 	'CLEANUP_ORPHANED':
			res = self.doCleanupOrphaned(uname, request)
		elif	action	 == 	'SET_G_LOCK':
			res	 = 	self.setGlobalLock(uname, request)	
		elif	action	 == 	'GET_G_LOCK':			
			res = self.doCheckGlobalLock()
		elif	action	 == 	'ALL_INTRATABLES':	
			res	 = 	self.getAllIntraTable(uname, request)
		elif	action	 == 	'ALL_USERNAMES':	
			res	 = 	self.getAllUserNames(uname, request)
		elif	action	 == 	'ALL_NEWTABLES':	
			res	 = 	self.getAllNewTables(uname, request)		
		else:
			hhtpstatus = status.HTTP_400_BAD_REQUEST
		
		
		
			
			
		return	Response(res, 	status=hhtpstatus)
		
	def	getAllIntraTable(self, 	uname, request):
		querystring	 = 	"select	tablename	from	pg_tables	where	not	tablename	like	'PUB%'	and	schemaname	=	'brugis_intra'	order	by	UPPER(tablename)"
		val	 = 	self.dbQueryExec(querystring)
		return	self.asJsonValue(self._jkeyFunction, val)	
	
	def	getAllUserNames(self, 	uname, request):
		querystring	 = 	"SELECT	distinct	username	FROM	{}.users	order	by	username".format(self._devSchema_admin)
		val	 = 	self.dbQueryExec(querystring)
		return	self.asJsonValue(self._jkeyFunction, val)	
	
	def	getAllUserTables(self, 	uname, request):
		if uname == "undefined":
			username	 = 	request.query_params.get('uname', 	None)
		else:
			username	 = 	uname
		querystring	 = 	"select table_name from {}.user_rights where user_name = \'{}\' order by table_name ;".format(self._devSchema_admin, username)
		val	 = 	self.dbQueryExec(querystring)
		return	self.asJsonValue(self._jkeyFunction, val)
	
	# # 
	#  @brief Brief
	#  
	#  @param [in] self    Parameter_Description
	#  @param [in] uname   Parameter_Description
	#  @param [in] request Parameter_Description
	#  @return Return_Description
	#  
	#  @details Details
	#  
	def	getAllNewTables(self, 	uname, request):		
		newtables	 = 	"select	tablename	from	pg_tables	where	schemaname	=	'brugis_edittmp'	and	tablename	not	in	(select	tablename	from	pg_tables	where	schemaname	=	'brugis_intra')"
		val	 = 	self.dbQueryExec(newtables)
		return	self.asJsonValue(self._jkeyFunction, val)
	
	
	def	doAssignLayer(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		username	 = 	request.query_params.get('uname', 	None)
		querystring	 = 	"insert	into	{}.user_rights	(	table_name,	schema_name,	user_name	)	values	(\'{}\',\'brugis_intra\',\'{}\')".format(self._devSchema_admin, layername, username)				
		self.dbRawExec(querystring)
		querystringdefault	 = 	"insert	into	{}.tables_states	(schema_name,	state,	user_name,	table_name)	values	(\'brugis_intra\',\'CIN\',\'{}\',\'{}\')".format(self._devSchema_admin, uname, layername)
		self.dbRawExec(querystringdefault)	
		return	"DONE"
		
		
	
		
	def	doTableDefaultAssign(self, 	uname, request):
		tbl	 = 	request.query_params.get('lname', 	None)		
		querystring	 = 	"insert	into	{}.user_rights	(	table_name,	schema_name,	user_name	)	values	(\'{}\',\'brugis_intra\',\'{}\')".format(self._devSchema_admin, tbl, uname)	
		self.dbRawExec(querystring)
		querystring	 = 	"insert	into	{}.tables_states	(schema_name,	state,	statecrea,	user_name,	table_name)	values	(\'brugis_intra\',\'COUT\',\'NEW\',\'{}\',\'{}\')".format(self._devSchema_admin, uname, 	tbl)
		self.dbRawExec(querystring)	
	
	def	doValidateImport(self, 	uname, request):
		tbl	 = 	request.query_params.get('lname', 	None)
		gtype	 = 	request.query_params.get('gtype', 	None)	
		
		querystring	 = 	'select * from brugis_edittmp.{} where not ST_ISVALID("GEOMETRY")'.format(tbl)	
		validres = self.dbQueryExec(querystring)
		if len(validres) > 0:
			print "doValidateImport INVALID DATA"
			return 'INVALID DATA'
		else:
			querystring	 = 	"commonbrugis.uppercase_table_attributes(\'brugis_edittmp\', \'{}')".format(tbl)
			self.dbRawExec(querystring)
			querystring	 = 	"commonbrugis.create_std_contraints(\'brugis_edittmp\', \'{}', \'{}')".format(tbl, gtype)
			self.dbRawExec(querystring)
		return 'DONE'
			
		
	def	doGetGeometryType(self, 	lname):
		querystring	 = 	"select	commonbrugis.getgeometrytype(\'brugis_edittmp\',\'{}\')".format(lname)
		self.dbRawExec(querystring)
	
		
	def doCleanupOrphaned(self, uname, request):
		querystring = "select commonbrugis.cleanup_orphaned()"
		self.dbRawExec(querystring)

		
	def	resetGlobalLock(self, uname, request):
		querystring	 = 	"update	{}.globalparams	set	value	=	\'FALSE\'	where	name	=	\'globallock\'	".format(self._devSchema_admin)
		self.dbRawExec(querystring)
	
	def	setGlobalLock(self, uname, request):
		querystring	 = 	"update	{}.globalparams	set	value	=	\'TRUE\'	where	name	=	\'globallock\'	".format(self._devSchema_admin)
		self.dbRawExec(querystring)
		
	def doCheckGlobalLock(self):
		lockquery = "select value from {}.globalparams where name = \'globallock\' and value = \'TRUE\'".format(self._devSchema_admin)
		val = self.dbQueryExecSingleton(lockquery)
		return	self.asJsonValue(self._jkeyFunction, val)
	
	
	def	doTransfertAllCheckout(self, 	uname, request):
		querystring	 = 	"select	commonbrugis.transfer_all_checkout(\'{}\')".format(self._adminuser)
		self.dbRawExec(querystring)
	
	def doPk(self, uname, request):
		lname	 = 	request.query_params.get('lname', 	None)
		query_toserial = "select commonbrugis.change_integer_pk_to_serial (\'{}\', \'{}\')".format(lname, self._devSchema_edit) ;
		query_setdefault = "select commonbrugis.change_pk_use_sequence(\'{}\', \'{}\')".format(lname, self._devSchema_edit) ;
		self.dbRawExec(query_toserial)
		self.dbRawExec(query_setdefault)
	
	
	def addGSLayer(self, uname, request):	
		lname	 = 	request.query_params.get('lname', 	None)
		geometrytype	 = 	self.doGetGeometryType(lname)
		gs = gsWrapper()
		res = gs.addLayer(lname, geometrytype)
		return	self.asJsonValue(self._jkeyFunction, res)
	
	def removeGSLayer(self, uname, request):
		lname	 = 	request.query_params.get('lname', 	None)
		gs = gsWrapper()
		res = gs.removeLayer(lname)
		return	self.asJsonValue(self._jkeyFunction, res)
		
	def	tableEditDrop(self, uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		therequest	 = 	"drop	table	\"{}\".\"{}\"".format(self._devSchema_modif, layername)
		self.dbRawExec(therequest)		
	
	
	def	removeUserRight(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		username	 = 	request.query_params.get('uname', 	None)
		print "removeUserRight {} {}".format(layername,username)
		deleterequest	 = 	"delete	from	{}.user_rights	where	table_name	=	\'{}\'	and	user_name	=	'{}\'".format(self._devSchema_admin, layername, username)
		self.dbRawExec(deleterequest)
	
	def	removeUserRightOnAllLayer(self, 	uname, request):
		username	 = 	request.query_params.get('uname', 	None)
		query	 = 	"delete	from	{1}.user_rights	where	user_name	=	\'{0}\'	and	table_name	not	in	(	select	table_name	from	{1}.tables_states	where	user_name	=	\'{0}\'	and	state	<>	'CIN')".format(username, self._devSchema_admin)
		self.dbRawExec(query)
		querystates	 = 	"delete	from	{0}.tables_states	where	user_name	not	in	(	select	user_name	from	{0}.user_rights)".format(self._devSchema_admin)
		print querystates
		self.dbRawExec(querystates)
		
		
	def	resetCreationStatus(self, 	uname, request):
		layername	 = 	request.query_params.get('lname', 	None)
		updaterequest	 = 	"update	{}.tables_states	set	statecrea	=	null	where	table_name	=	\'{}\'".format(self._devSchema_admin, layername)
		self.dbRawExec(updaterequest)
		
	def isUserEditGranted(self):
		grantedrequest = "select commonbrugis.isbrugiseditorgrantee()"
		return self.dbRawExec(grantedrequest)

	def	doCheckConsistency(self, uname, request):
		username	 = 	uname
		consitencyquery	 = 	"select	table_name	from	{}.tables_states	where	user_name	=	\'{}\'	and	state	<>	'CIN'	AND	table_name	not	in	(select	tablename	from	pg_tables	where	schemaname	=	'brugis_edittmp'	OR	schemaname	=	'brugis_modif'	)".format(self._devSchema_admin, username)
		val	 = 	self.dbQueryExec(consitencyquery)
		return	self.asJsonValue(self._jkeyFunction, val)
	
	def	createUser(self, adminuname, request):
		user	 = 	request.query_params.get('uname', 	None)
		pswd	 = 	request.query_params.get('upswd', 	None)
		mail	 = 	request.query_params.get('umail', 	None)
		#######
		# # Does nothing !!! but force change in searchpath
		self.dbRawExec('select * from users', 'brugis_qgisplugin_admin')
		
		user	 = 	User.objects.create_user(username='{}'.format(user),
												email='{}'.format(mail),
												password='{}'.format(pswd))
		sqlStatement	 = 	"insert	into	{}.users	(username,	userpswd,	usermail)	values	(\'{}\',\'{}\',\'{}\')".format(self._devSchema_admin, user, pswd, mail)
		self.dbRawExec(sqlStatement, 'brugis_qgisplugin_admin')
	
	def	updateUser(self, adminuname, request):
		user	 = 	request.query_params.get('uname', 	None)
		userpswd	 = 	request.query_params.get('upswd', 	None)
		usermail	 = 	request.query_params.get('umail', 	None)
		
		sqlStatement	 = 	"update	{}.users set slock=0, userpswd=	\'{}\',	usermail= \'{}\' where username= \'{}\'".format(self._devSchema_admin, userpswd, usermail, user)
		self.dbRawExec(sqlStatement, 'brugis_qgisplugin_admin')	
		try:
			u = User.objects.get(username=user)
			u.set_password(userpswd)
			u.email = usermail
			u.save()
		except Exception as e:
			user = 	User.objects.create_user(username='{}'.format(user),
												email='{}'.format(usermail),
												password='{}'.format(userpswd))
			
		
		
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
	
	
	
	
	def	doDeleteUser(self, adminuname, request):
		uname	 = 	request.query_params.get('uname', 	None)
		try:
			self.dbSetSearchPath(self._devSchema_admin)
			print "delete step 1"
			u = User.objects.get(username=uname)
			u.delete()
			print "delete step 2"
			statequery_ts	 = 	"delete	from	{}.tables_states	where	user_name	=\'{}\'	".format(self._devSchema_admin, uname)
			self.dbRawExec(statequery_ts)
			print "delete step 3"
			statequery_ur	 = 	"delete	from	{}.user_rights	where	user_name	=\'{}\'	".format(self._devSchema_admin, uname)
			self.dbRawExec(statequery_ur)
			print "delete step 4"
			statequery_u	 = 	"delete	from	{}.users	where	username	=\'{}\'	".format(self._devSchema_admin, uname)
			self.dbRawExec(statequery_u)
			print "delete step 5"
		except Exception as e:
			print e.message
			print "unknown user"
		
		
	
		
	def	doBrugisEvent(self, 	uname, request):
		params	 = 	request.query_params
		lname	 = 	params.get('layername', 	None)
		baction	 = 	params.get('trans', 	None)
		state	 = 	params.get('state', 	None)
		res	 = 	params.get('result', 	None)	
		info	 = 	params.get('info', 	None)
		
		context	 = 	"BdmWebAccess"
		
		hname	 = 	request.META['REMOTE_ADDR']
		
		eventQuery	 = 	"""insert	into	{}.events(
		user_name,	table_name,	action,	initialstate,	context,	result,	
		info,	client)	VALUES	('{}',	'{}',	'{}',	'{}',	'{}',	'{}',	'{}',	'{}')""".format(self._devSchema_admin, uname, 	lname, baction, state, context	 + 	"_"	 + 	self._myVersion, res, info, hname)
		self.dbRawExec(eventQuery)
	
	#####################################
	# 	Django is not "schema friendly" 
	#   this little trick allows Django to retrieve the right schema  
	def	dbSetSearchPath(self, searchpath='public'):
		# Manager.raw(querystring)
		with	connection.cursor()	as	cursor:
				cursor.execute('SET search_path TO {}'.format(searchpath))
				
	#####################################
	# 	Methodes	utilitaires
	def	dbRawExec(self, querystring, searchpath='public'):
		# Manager.raw(querystring)
		with	connection.cursor()	as	cursor:
				cursor.execute('SET search_path TO {}'.format(searchpath))
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
		
	# # 
	#  @brief Brief
	#  
	#  @param [in] self   Parameter_Description
	#  @param [in] cursor Parameter_Description
	#  @return Return all rows from a cursor as a namedtuple
	#  
	#  @details Details
	#  	
	def	namedtuplefetchall(self, cursor):
		""
		desc	 = 	cursor.description
		nt_result	 = 	namedtuple('results', 	[col[0]	for	col	in	desc])
		return	[nt_result(*row)	for	row	in	cursor.fetchall()]	
	
	# #
	#
	# Convert name\ value pair as dictionary
	def	asJsonValue(self, name, 	value):
		d	 = 	{name:	value}
		return	d
	
	
