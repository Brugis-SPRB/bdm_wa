## 
# @file serializers.py
# @brief Bdm Project | Web Access Subsystem | django serializers implementation
# @author Michel Van Asten

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import UserRights,UserInfos,UserTableStates,TableStates

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
		
class UserInfosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInfos
        fields = ('username', 'userpswd', 'userrole', 'slock', 'usermail')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
		
class TableStatesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
		model = TableStates
		fields = ('table_name', 'schema_name', 'user_name', 'state', 'statecrea')

class UserTableStatesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = UserTableStates
		fields = ('table_name', 'schema', 'uname', 'state')		
		
class UserRightsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserRights
        fields = ('user_name', 'schema_name', 'table_name')
		