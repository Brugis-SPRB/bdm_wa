# # 
#  @file views.py
#  @brief Bdm Project | Web Access Subsystem | Django views implementation
#  @author Michel Van Asten
#  
from django.contrib.auth.models import User, Group
import django_filters.rest_framework as filters
from rest_framework import viewsets

from bdmcore.serializers import UserSerializer, GroupSerializer, UserRightsSerializer, TableStatesSerializer, UserTableStatesSerializer, UserInfosSerializer
from models import UserInfos, UserRights, UserTableStates, TableStates


class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	
class UserInfoViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = UserInfos.objects.all().order_by('username')
	serializer_class = UserInfosSerializer
	filter_fields = ('username',)	


class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	
class UserRightsViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = UserRights.objects.all()
	serializer_class = UserRightsSerializer
	
class TableStatesViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = TableStates.objects.all()
	serializer_class = TableStatesSerializer
	
	
class UserTableStatesViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = UserTableStates.objects.all()
	serializer_class = UserTableStatesSerializer
	filter_fields = ('uname',)

	
