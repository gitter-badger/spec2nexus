#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''prjPySpec plugins for control lines defined by APS UNICAT'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


from spec2nexus.plugin import ControlLineHandler, strip_first_word


class MetadataMnes(ControlLineHandler):
    key_regexp = '#H\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.H.append( strip_first_word(text).split() )


class MetadataValues(ControlLineHandler):
    key_regexp = '#V\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.V.append( strip_first_word(text) )       # TODO: what about post-processing?
