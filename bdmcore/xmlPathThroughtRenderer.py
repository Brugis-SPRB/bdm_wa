  # -*- coding: utf-8 -*-

# # 
# @file models.py
# @brief Bdm Project | Web Access Subsystem 
# @author Michel Van Asten

from rest_framework import renderers


# #
# set format and media_type... Just to avoid any tranformation of previously generated XML
#
class xmlPathThroughtRenderer(renderers.BaseRenderer):
    media_type = 'text/xml'
    format = 'xml'

    def render(self, data, media_type=None, renderer_context=None):
        try:
            return data.encode(self.charset)
        except Exception, e :
            return data
