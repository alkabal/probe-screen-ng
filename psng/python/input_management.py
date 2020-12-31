#!/usr/bin/env python
#
# Copyright (c) 2015 Serguei Glavatski ( verser  from cnc-club.ru )
# Copyright (c) 2020 Probe Screen NG Developers
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; If not, see <http://www.gnu.org/licenses/>.

import os
import sys

import hal
import hal_glib
import time

from .base import ProbeScreenBase


class ProbeScreenInputManagement(ProbeScreenBase):
    # --------------------------
    #
    #  INIT
    #
    # --------------------------
    def __init__(self, halcomp, builder, useropts):
        super(ProbeScreenInputManagement, self).__init__(halcomp, builder, useropts)

        # make the pins for tool measurement
        self.halcomp.newpin("probe_inhibited", hal.HAL_BIT, hal.HAL_OUT)
        self.halcomp.newpin("setter_inhibited", hal.HAL_BIT, hal.HAL_OUT)


        pin2 = self.halcomp.newpin("probe_connected", hal.HAL_BIT, hal.HAL_IN)
        hal_glib.GPin(pin2).connect("value_changed", self.inhibit_probe)
        
        pin3 = self.halcomp.newpin("setter_connected", hal.HAL_BIT, hal.HAL_IN)
        hal_glib.GPin(pin3).connect("value_changed", self.inhibit_setter)
        

    def inhibit_probe(self, gtkbutton, data=None):  
          if self.halcomp["probe_connected"] == 0:
               self.halcomp["probe_inhibited"] = 1
          else:
               self.halcomp["probe_inhibited"] = 0
       
    def inhibit_setter(self, gtkbutton, data=None):  
          if self.halcomp["setter_connected"] == 0:
               self.halcomp["setter_inhibited"] = 1
          else:
               self.halcomp["setter_inhibited"] = 0
        
        
        
