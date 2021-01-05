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

from .base import ProbeScreenBase


class ProbeScreenWorkpieceMeasurement(ProbeScreenBase):

    # --------------------------
    #
    #  INIT
    #
    # --------------------------
    def __init__(self, halcomp, builder, useropts):
        super(ProbeScreenWorkpieceMeasurement, self).__init__(
            halcomp, builder, useropts
        )

        self.xpym = self.builder.get_object("xpym")
        self.ym = self.builder.get_object("ym")
        self.xmym = self.builder.get_object("xmym")
        self.xp = self.builder.get_object("xp")
        self.center = self.builder.get_object("center")
        self.xm = self.builder.get_object("xm")
        self.xpyp = self.builder.get_object("xpyp")
        self.yp = self.builder.get_object("yp")
        self.xmyp = self.builder.get_object("xmyp")
        self.hole = self.builder.get_object("hole")

    # --------------  Command buttons -----------------
    #               Measurement outside
    # -------------------------------------------------
    # X+
    def on_xp_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move X - xy_clearance
             s = """G91
             G1 X-%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"]
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xplus.ngc
             if self.ocode("o<psng_xplus> call") == -1:
                 return
             a = self.probed_position_with_offsets()
             xres = float(a[0] + 0.5 * self.halcomp["ps_probe_diam"])
             self.display_result_xp(xres)
             self.lenght_x()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XpLx",
                 0,
                 0,
                 xres,
                 self.lenght_x(),
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
             )
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 X%f" % (xres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("X")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return
             
    # Y+
    def on_yp_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move Y - xy_clearance
             s = """G91
             G1 Y-%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"]
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_yplus.ngc
             if self.ocode("o<psng_yplus> call") == -1:
                 return
             a = self.probed_position_with_offsets()
             yres = float(a[1]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_yp(yres)
             self.lenght_y()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "YpLy",
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 yres,
                 self.lenght_y(),
                 0,
                 0,
                 0,
             )
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 Y%f" % (yres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("Y")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # X-
    def on_xm_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move X + xy_clearance
             s = """G91
             G1 X%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"]
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xminus.ngc
             if self.ocode("o<psng_xminus> call") == -1:
                 return
             a = self.probed_position_with_offsets()
             xres = float(a[0] - 0.5 * self.halcomp["ps_probe_diam"])
             self.display_result_xm(xres)
             self.lenght_x()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XmLx",
                 xres,
                 0,
                 0,
                 self.lenght_x(),
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
             )
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 X%f" % (xres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("X")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # Y-
    def on_ym_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move Y + xy_clearance
             s = """G91
             G1 Y%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"]
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_yminus.ngc
             if self.ocode("o<psng_yminus> call") == -1:
                 return
             a = self.probed_position_with_offsets()
             yres = float(a[1]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_ym(yres)
             self.lenght_y()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "YmLy",
                 0,
                 0,
                 0,
                 0,
                 yres,
                 0,
                 0,
                 self.lenght_y(),
                 0,
                 0,
                 0,
             )
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 Y%f" % (yres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("Y")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # Corners
    # Move Probe manual under corner 2-3 mm
    # X+Y+
    def on_xpyp_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move X - xy_clearance Y + edge_lenght
             s = """G91
             G1 X-%f Y%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"],
                 self.halcomp["ps_edge_lenght"],
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xplus.ngc
             if self.ocode("o<psng_xplus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xres = float(a[0] + 0.5 * self.halcomp["ps_probe_diam"])
             self.display_result_xp(xres)
             self.lenght_x()
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             
             # move X + edge_lenght +xy_clearance,  Y - edge_lenght - xy_clearance
             tmpxy = self.halcomp["ps_edge_lenght"] + self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 X%f Y-%f
             G90""" % (
                 tmpxy,
                 tmpxy,
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_yplus.ngc
             if self.ocode("o<psng_yplus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             yres = float(a[1]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_yp(yres)
             self.lenght_y()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XpLxYpLy",
                 0,
                 0,
                 xres,
                 self.lenght_x(),
                 0,
                 0,
                 yres,
                 self.lenght_y(),
                 0,
                 0,
                 0,
             )
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 X%f Y%f" % (xres, yres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("XY")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # X+Y-
    def on_xpym_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move X - xy_clearance Y + edge_lenght
             s = """G91
             G1 X-%f Y-%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"],
                 self.halcomp["ps_edge_lenght"],
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xplus.ngc
             if self.ocode("o<psng_xplus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xres = float(a[0] + 0.5 * self.halcomp["ps_probe_diam"])
             self.display_result_xp(xres)
             self.lenght_x()
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             
             # move X + edge_lenght +xy_clearance,  Y + edge_lenght + xy_clearance
             tmpxy = self.halcomp["ps_edge_lenght"] + self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 X%f Y%f
             G90""" % (
                 tmpxy,
                 tmpxy,
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_yminus.ngc
             if self.ocode("o<psng_yminus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             yres = float(a[1]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_ym(yres)
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XpLxYmLy",
                 0,
                 0,
                 xres,
                 self.lenght_x(),
                 yres,
                 0,
                 0,
                 self.lenght_y(),
                 0,
                 0,
                 0,
             )
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 X%f Y%f" % (xres, yres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("XY")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # X-Y+
    def on_xmyp_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move X + xy_clearance Y + edge_lenght
             s = """G91
             G1 X%f Y%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"],
                 self.halcomp["ps_edge_lenght"],
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xminus.ngc
             if self.ocode("o<psng_xminus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xres = float(a[0] - 0.5 * self.halcomp["ps_probe_diam"])
             self.display_result_xm(xres)
             self.lenght_x()
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             
             # move X - edge_lenght - xy_clearance,  Y - edge_lenght - xy_clearance
             tmpxy = self.halcomp["ps_edge_lenght"] + self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 X-%f Y-%f
             G90""" % (
                 tmpxy,
                 tmpxy,
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_yplus.ngc
             if self.ocode("o<psng_yplus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             yres = float(a[1]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_yp(yres)
             self.lenght_y()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XmLxYpLy",
                 xres,
                 0,
                 0,
                 self.lenght_x(),
                 0,
                 0,
                 yres,
                 self.lenght_y(),
                 0,
                 0,
                 0,
             )
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 X%f Y%f" % (xres, yres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("XY")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # X-Y-
    def on_xmym_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move X + xy_clearance Y - edge_lenght
             s = """G91
             G1 X%f Y-%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"],
                 self.halcomp["ps_edge_lenght"],
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xminus.ngc
             if self.ocode("o<psng_xminus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xres = float(a[0] - 0.5 * self.halcomp["ps_probe_diam"])
             self.display_result_xm(xres)
             self.lenght_x()
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             
             # move X - edge_lenght - xy_clearance,  Y + edge_lenght + xy_clearance
             tmpxy = self.halcomp["ps_edge_lenght"] + self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 X-%f Y%f
             G90""" % (
                 tmpxy,
                 tmpxy,
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_yminus.ngc
             if self.ocode("o<psng_yminus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             yres = float(a[1]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_ym(yres)
             self.lenght_y()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XmLxYmLy",
                 xres,
                 0,
                 0,
                 self.lenght_x(),
                 yres,
                 0,
                 0,
                 self.lenght_y(),
                 0,
                 0,
                 0,
             )
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 X%f Y%f" % (xres, yres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("XY")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # Center X+ X- Y+ Y-
    def on_xy_center_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move X - edge_lenght- xy_clearance
             tmpx = self.halcomp["ps_edge_lenght"] + self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 X-%f
             G90""" % (
                 tmpx
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xplus.ngc
             if self.ocode("o<psng_xplus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xpres = float(a[0]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_xp(xpres)
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             
             # move X + 2 edge_lenght + 2 xy_clearance
             tmpx = 2 * (self.halcomp["ps_edge_lenght"] + self.halcomp["ps_xy_clearance"])
             s = """G91
             G1 X%f
             G90""" % (
                 tmpx
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xminus.ngc
             
             if self.ocode("o<psng_xminus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xmres = float(a[0]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_xm(xmres)
             self.lenght_x()
             xcres = 0.5 * (xpres + xmres)
             self.display_result_xc(xcres)
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             # distance to the new center of X from current position
             #        self.stat.poll()
             #        to_new_xc=self.stat.position[0]-self.stat.g5x_offset[0] - self.stat.g92_offset[0] - self.stat.tool_offset[0] - xcres
             s = "G1 X%f" % (xcres)
             if self.gcode(s) == -1:
                 return
             
             # move Y - edge_lenght- xy_clearance
             tmpy = self.halcomp["ps_edge_lenght"] + self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 Y-%f
             G90""" % (
                 tmpy
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_yplus.ngc
             if self.ocode("o<psng_yplus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             ypres = float(a[1]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_yp(ypres)
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             
             # move Y + 2 edge_lenght + 2 xy_clearance
             tmpy = 2 * (self.halcomp["ps_edge_lenght"] + self.halcomp["ps_xy_clearance"])
             s = """G91
             G1 Y%f
             G90""" % (
                 tmpy
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_yminus.ngc
             if self.ocode("o<psng_yminus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             ymres = float(a[1]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_ym(ymres)
             self.lenght_y()
             # find, show and move to finded  point
             ycres = 0.5 * (ypres + ymres)
             self.display_result_yc(ycres)
             diam = ymres - ypres
             self.display_result_d(diam)
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XmXcXpLxYmYcYpLyD",
                 xmres,
                 xcres,
                 xpres,
                 self.lenght_x(),
                 ymres,
                 ycres,
                 ypres,
                 self.lenght_y(),
                 0,
                 diam,
                 0,
             )
             # move Z to start point up
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 Y%f" % (ycres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("XY")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # --------------  Command buttons -----------------
    #               Measurement inside
    # -------------------------------------------------

    # Corners
    # Move Probe manual under corner 2-3 mm
    # X+Y+
    def on_xpyp1_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move Y - edge_lenght X - xy_clearance
             s = """G91
             G1 X-%f Y-%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"],
                 self.halcomp["ps_edge_lenght"],
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xplus.ngc
             if self.ocode("o<psng_xplus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xres = float(a[0]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_xp(xres)
             self.lenght_x()
             
             # move X - edge_lenght Y - xy_clearance
             tmpxy = self.halcomp["ps_edge_lenght"] - self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 X-%f Y%f
             G90""" % (
                 tmpxy,
                 tmpxy,
             )
             if self.gcode(s) == -1:
                 return
             # Start psng_yplus.ngc
             if self.ocode("o<psng_yplus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             yres = float(a[1]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_yp(yres)
             self.lenght_y()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XpLxYpLy",
                 0,
                 0,
                 xres,
                 self.lenght_x(),
                 0,
                 0,
                 yres,
                 self.lenght_y(),
                 0,
                 0,
                 0,
             )
             # move Z to start point
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 X%f Y%f" % (xres, yres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("XY")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # X+Y-
    def on_xpym1_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move Y + edge_lenght X - xy_clearance
             s = """G91
             G1 X-%f Y%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"],
                 self.halcomp["ps_edge_lenght"],
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xplus.ngc
             if self.ocode("o<psng_xplus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xres = float(a[0]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_xp(xres)
             self.lenght_x()
             
             # move X - edge_lenght Y + xy_clearance
             tmpxy = self.halcomp["ps_edge_lenght"] - self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 X-%f Y-%f
             G90""" % (
                 tmpxy,
                 tmpxy,
             )
             if self.gcode(s) == -1:
                 return
             # Start psng_yminus.ngc
             if self.ocode("o<psng_yminus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             yres = float(a[1]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_ym(yres)
             self.lenght_y()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XpLxYmLy",
                 0,
                 0,
                 xres,
                 self.lenght_x(),
                 yres,
                 0,
                 0,
                 self.lenght_y(),
                 0,
                 0,
                 0,
             )
             # move Z to start point
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 X%f Y%f" % (xres, yres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("XY")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # X-Y+
    def on_xmyp1_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move Y - edge_lenght X + xy_clearance
             s = """G91
             G1 X%f Y-%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"],
                 self.halcomp["ps_edge_lenght"],
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xminus.ngc
             if self.ocode("o<psng_xminus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xres = float(a[0]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_xm(xres)
             self.lenght_x()
             
             # move X + edge_lenght Y - xy_clearance
             tmpxy = self.halcomp["ps_edge_lenght"] - self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 X%f Y%f
             G90""" % (
                 tmpxy,
                 tmpxy,
             )
             if self.gcode(s) == -1:
                 return
             # Start psng_yplus.ngc
             if self.ocode("o<psng_yplus> call") == -1:
                 return
             
             # show Y result
             a = self.probed_position_with_offsets()
             yres = float(a[1]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_yp(yres)
             self.lenght_y()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XmLxYpLy",
                 xres,
                 0,
                 0,
                 self.lenght_x(),
                 0,
                 0,
                 yres,
                 self.lenght_y(),
                 0,
                 0,
                 0,
             )
             # move Z to start point
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 X%f Y%f" % (xres, yres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("XY")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # X-Y-
    def on_xmym1_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             # move Y + edge_lenght X + xy_clearance
             s = """G91
             G1 X%f Y%f
             G90""" % (
                 self.halcomp["ps_xy_clearance"],
                 self.halcomp["ps_edge_lenght"],
             )
             if self.gcode(s) == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # Start psng_xminus.ngc
             if self.ocode("o<psng_xminus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xres = float(a[0]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_xm(xres)
             self.lenght_x()
             
             # move X + edge_lenght Y - xy_clearance
             tmpxy = self.halcomp["ps_edge_lenght"] - self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 X%f Y-%f
             G90""" % (
                 tmpxy,
                 tmpxy,
             )
             if self.gcode(s) == -1:
                 return
             # Start psng_yminus.ngc
             if self.ocode("o<psng_yminus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             yres = float(a[1]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_ym(yres)
             self.lenght_y()
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XmLxYmLy",
                 xres,
                 0,
                 0,
                 self.lenght_x(),
                 yres,
                 0,
                 0,
                 self.lenght_y(),
                 0,
                 0,
                 0,
             )
             # move Z to start point
             if self.z_clearance_up() == -1:
                 return
             # move to finded  point
             s = "G1 X%f Y%f" % (xres, yres)
             if self.gcode(s) == -1:
                 return
             self.set_zerro("XY")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return

    # Hole Xin- Xin+ Yin- Yin+
    def on_xy_hole_released(self, gtkbutton, data=None):
        if self.error_poll() == 0:
             if self.ocode("o<psng_hook> call [7]") == -1:
                 return
             if self.z_clearance_down() == -1:
                 return
             # move X - edge_lenght Y + xy_clearance
             tmpx = self.halcomp["ps_edge_lenght"] - self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 X-%f
             G90""" % (
                 tmpx
             )
             if self.gcode(s) == -1:
                 return
             # Start psng_xminus.ngc
             if self.ocode("o<psng_xminus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xmres = float(a[0]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_xm(xmres)
             
             # move X +2 edge_lenght - 2 xy_clearance
             tmpx = 2 * (self.halcomp["ps_edge_lenght"] - self.halcomp["ps_xy_clearance"])
             s = """G91
             G1 X%f
             G90""" % (
                 tmpx
             )
             if self.gcode(s) == -1:
                 return
             # Start psng_xplus.ngc
             if self.ocode("o<psng_xplus> call") == -1:
                 return
             # show X result
             a = self.probed_position_with_offsets()
             xpres = float(a[0]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_xp(xpres)
             self.lenght_x()
             xcres = 0.5 * (xmres + xpres)
             self.display_result_xc(xcres)
             
             # move X to new center
             s = """G1 X%f""" % (xcres)
             if self.gcode(s) == -1:
                 return
             
             # move Y - edge_lenght + xy_clearance
             tmpy = self.halcomp["ps_edge_lenght"] - self.halcomp["ps_xy_clearance"]
             s = """G91
             G1 Y-%f
             G90""" % (
                 tmpy
             )
             if self.gcode(s) == -1:
                 return
             # Start psng_yminus.ngc
             if self.ocode("o<psng_yminus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             ymres = float(a[1]) - 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_ym(ymres)
             
             # move Y +2 edge_lenght - 2 xy_clearance
             tmpy = 2 * (self.halcomp["ps_edge_lenght"] - self.halcomp["ps_xy_clearance"])
             s = """G91
             G1 Y%f
             G90""" % (
                 tmpy
             )
             if self.gcode(s) == -1:
                 return
             # Start psng_yplus.ngc
             if self.ocode("o<psng_yplus> call") == -1:
                 return
             # show Y result
             a = self.probed_position_with_offsets()
             ypres = float(a[1]) + 0.5 * self.halcomp["ps_probe_diam"]
             self.display_result_yp(ypres)
             self.lenght_y()
             # find, show and move to finded  point
             ycres = 0.5 * (ymres + ypres)
             self.display_result_yc(ycres)
             diam = 0.5 * ((xpres - xmres) + (ypres - ymres))
             self.display_result_d(diam)
             self.add_history(
                 gtkbutton.get_tooltip_text(),
                 "XmXcXpLxYmYcYpLyD",
                 xmres,
                 xcres,
                 xpres,
                 self.lenght_x(),
                 ymres,
                 ycres,
                 ypres,
                 self.lenght_y(),
                 0,
                 diam,
                 0,
             )
             # move to center
             s = "G1 Y%f" % (ycres)
             if self.gcode(s) == -1:
                 return
             # move Z to start point
             if self.z_clearance_up() == -1:
                 return
             self.set_zerro("XY")
             if self.ocode("o<psng_hook_end> call") == -1:
                 return
