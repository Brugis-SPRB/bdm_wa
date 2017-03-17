# -*- coding: utf-8 -*-

# # 
# @file models.py
# @brief Bdm Project | Web Access Subsystem | django model implementation
# @note persistance in brugis_qgisplugin_admin schema 
# @author Michel Van Asten

from __future__ import unicode_literals

from django.db import models


# #
# 
# User \ Layer assignment 
class UserRights(models.Model):
	user_name = models.CharField(max_length=50)
	table_name = models.CharField(max_length=50)
	schema_name = models.CharField(max_length=100)
	class Meta:
		db_table = 'user_rights'

# #
# 
# User metadata
class UserInfos(models.Model):
	username = models.CharField(max_length=50)
	userrole = models.CharField(max_length=50)
	userpswd = models.CharField(max_length=30)
	slock = models.IntegerField()
	usermail = models.CharField(max_length=50)
	class Meta:
		db_table = 'users'

# #
# 
# Brugis table states
class TableStates(models.Model):	
	table_name = models.CharField(max_length=50)
	schema_name = models.CharField(max_length=30)
	user_name = models.CharField(max_length=50)
	state = models.CharField(max_length=10)
	statecrea = models.CharField(max_length=20)
	class Meta:
		managed = False
		db_table = 'tables_states'
# #
# 
# Brugis table states (view)
class UserTableStates(models.Model):
	table_name = models.CharField(max_length=50)
	schema = models.CharField(max_length=30)
	uname = models.CharField(max_length=50)
	state = models.CharField(max_length=10)
	class Meta:
		managed = False
		db_table = 'user_tablestates'
		
# #
#
# Brugis table states (view)
class events(models.Model):		
	user_name = models.CharField(max_length=20),
	table_name = models.CharField(max_length=30)
	action = models.CharField(max_length=20)
	initialstate = models.CharField(max_length=20)
	context = models.CharField(max_length=20)
	result = models.CharField(max_length=10)
	info = models.CharField(max_length=200)
	client = models.CharField(max_length=100)
	class Meta:
		managed = False
		db_table = 'events'
# #
#
# Brugis table states (view)		
class globalparams(models.Model):		
	name = models.CharField(max_length=30)
	value = models.CharField(max_length=40)
	class Meta:
		managed = False
		db_table = 'globalparams'
		
