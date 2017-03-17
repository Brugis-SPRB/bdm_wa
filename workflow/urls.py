# -*- coding: utf-8 -*-

## 
#  @file urls.py
#  @brief Bdm Project | Web Access Subsystem | url mappings
#  @author Michel Van Asten
#  

from django.conf.urls import url, include
from rest_framework import routers
from bdmcore import views
from bdmcore import bdmCommandView
from bdmcore import bdmAdminCommandView
from bdmcore import bdmGeoServerProxy




router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'userinfos', views.UserInfoViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'userrights', views.UserRightsViewSet)
router.register(r'tablestates', views.TableStatesViewSet)
router.register(r'usertablestates', views.UserTableStatesViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

##
# Any url pattern must be defined here and associated to a specific view
# Note the use of regular expressions to capture some specific parameters like token (key) to be used for WFS calls
urlpatterns = [
    url(r'^', include(router.urls)),
	url(r'^command/', bdmCommandView.BdmCommandView.as_view(), name='BdmCommandView'),
	url(r'^admincommand/', bdmAdminCommandView.BdmAdminCommandView.as_view(), name='BdmAdminCommandView'),
	url(r'^token/', bdmCommandView.BdmKeyView.as_view(), name='BdmKeyView'),
	url(r'^map/(?P<key>([0-9a-fA-F]*-*)*)/', bdmGeoServerProxy.BdmWfsProxy.as_view(),name='BdmWfsProxy' ),
    url(r'^mapconfig/rest/', bdmGeoServerProxy.BdmRestProxy.as_view(),name='BdmRestProxy' ),    
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]