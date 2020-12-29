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

from .base import ProbeScreenBase


class ProbeScreenToolMeasurement(ProbeScreenBase):
    # --------------------------
    #
    #  INIT
    #
    # --------------------------
    def __init__(self, halcomp, builder, useropts):
        super(ProbeScreenToolMeasurement, self).__init__(halcomp, builder, useropts)

        self.hal_led_rotate_spindle = self.builder.get_object("hal_led_rotate_spindle")
        self.hal_led_set_m6 = self.builder.get_object("hal_led_set_m6")
        self.frm_probe_pos = self.builder.get_object("frm_probe_pos")
        self.spbtn_setter_height = self.builder.get_object("spbtn_setter_height")
        self.spbtn_block_height = self.builder.get_object("spbtn_block_height")
        self.btn_probe_tool_setter = self.builder.get_object("btn_probe_tool_setter")
        self.btn_probe_workpiece = self.builder.get_object("btn_probe_workpiece")
        self.tooledit1 = self.builder.get_object("tooledit1")
        self.chk_use_tool_measurement = self.builder.get_object(
            "chk_use_tool_measurement"
        )
        self.tool_dia = self.builder.get_object("tool_dia")
        self.down = self.builder.get_object("down")                                                       # It is something outdated ?

        self.chk_use_tool_measurement.set_active(
            self.prefs.getpref("use_toolmeasurement", False, bool)
        )

        self.chk_use_rotate_spindle = self.builder.get_object(
            "chk_use_rotate_spindle"
        )
        
        # make the pins for tool measurement
        self.halcomp.newpin("use_toolmeasurement", hal.HAL_BIT, hal.HAL_OUT)
        self.halcomp.newpin("probedtable", hal.HAL_FLOAT, hal.HAL_OUT)
        self.halcomp.newpin("setterheight", hal.HAL_FLOAT, hal.HAL_OUT)
        self.halcomp.newpin("blockheight", hal.HAL_FLOAT, hal.HAL_OUT)
        # for manual tool change dialog
        self.halcomp.newpin("toolchange-number", hal.HAL_S32, hal.HAL_IN)
        self.halcomp.newpin("toolchange-prep-number", hal.HAL_S32, hal.HAL_IN)
        self.halcomp.newpin("toolchange-changed", hal.HAL_BIT, hal.HAL_OUT)
        pin = self.halcomp.newpin("toolchange-change", hal.HAL_BIT, hal.HAL_IN)
        hal_glib.GPin(pin).connect("value_changed", self.on_tool_change)

        if self.chk_use_tool_measurement.get_active():
            self.halcomp["use_toolmeasurement"] = True
            self.hal_led_set_m6.hal_pin.set(1)

        self.halcomp.newpin("toolchange-diameter", hal.HAL_FLOAT, hal.HAL_IN)
        self.halcomp.newpin("use_rotate_spindle", hal.HAL_BIT, hal.HAL_OUT)
        
        if self.chk_use_rotate_spindle.get_active():
            self.halcomp["use_rotate_spindle"] = True
            self.hal_led_rotate_spindle.hal_pin.set(1)
            
        self._init_tool_sensor_data()

    # Read the ini file config [TOOLSENSOR] section
    def _init_tool_sensor_data(self):
        self.xpos = float(self.inifile.find("TOOLSENSOR", "X"))
        self.ypos = float(self.inifile.find("TOOLSENSOR", "Y"))
        self.zpos = float(self.inifile.find("TOOLSENSOR", "Z"))
        self.maxprobe = float(self.inifile.find("TOOLSENSOR", "MAXPROBE"))
        self.tsdiam = float(self.inifile.find("TOOLSENSOR", "TS_DIAMETER"))
        self.tsoffset = float(self.inifile.find("TOOLSENSOR", "TS_DIAM_OFFSET"))
        self.revrott = float(self.inifile.find("TOOLSENSOR", "REV_ROTATION_SPEED"))

        self.spbtn_setter_height.set_value(self.prefs.getpref("setterheight", 0.0, float))
        self.halcomp["setterheight"] = self.spbtn_setter_height.get_value()

        self.spbtn_block_height.set_value(self.prefs.getpref("blockheight", 0.0, float))
        self.halcomp["blockheight"] = self.spbtn_block_height.get_value()
        
        if (
            not self.xpos
            or not self.ypos
            or not self.zpos
            or not self.maxprobe
            or not self.tsdiam
            or not self.tsoffset
            or not self.revrott
        ):
            self.chk_use_tool_measurement.set_active(False)
            self.tool_dia.set_sensitive(False)
            print(_("**** PROBE SCREEN INFO ****"))
            print(_("**** no valid probe config in INI File ****"))
            print(_("**** disabled auto tool measurement ****"))
        else:
            # to set the hal pin with correct values we emit a toogled
            if self.chk_use_tool_measurement.get_active():
                self.frm_probe_pos.set_sensitive(False)
                self.halcomp["use_toolmeasurement"] = True
            else:
                self.frm_probe_pos.set_sensitive(True)
                self.chk_use_tool_measurement.set_sensitive(True)

    # ----------------
    # Remap M6 Buttons
    # ----------------
    # Tickbox from gui for enable disable remap (with saving pref)
    # Logic is now inverted for set.sensitive this is more logic : when remap is enabled you can't change settings so setting to be done before activate remap.
    def on_chk_use_tool_measurement_toggled(self, gtkcheckbutton, data=None):
        if gtkcheckbutton.get_active():
            self.frm_probe_pos.set_sensitive(False)
            self.halcomp["use_toolmeasurement"] = True
            self.halcomp["use_rotate_spindle"] = False
        else:
            self.frm_probe_pos.set_sensitive(True)
            self.halcomp["use_toolmeasurement"] = False
        self.prefs.putpref("use_toolmeasurement", gtkcheckbutton.get_active(), bool)
        self.hal_led_set_m6.hal_pin.set(gtkcheckbutton.get_active())

    # Set rotating spindle check (without saving pref)
    def on_chk_use_rotate_spindle_toggled(self, gtkcheckbutton, data=None):
        if gtkcheckbutton.get_active():
            self.halcomp["use_rotate_spindle"] = True
            self.hal_led_rotate_spindle.hal_pin.set(gtkcheckbutton.get_active())
        else:
            self.halcomp["use_rotate_spindle"] = False
            self.hal_led_rotate_spindle.hal_pin.set(gtkcheckbutton.get_active()) 
        
  

    # Spinbox for setter height with autosave value inside machine pref file
    def on_spbtn_setter_height_key_press_event(self, gtkspinbutton, data=None):
        self.on_common_spbtn_key_press_event("setterheight", gtkspinbutton, data)

    def on_spbtn_setter_height_value_changed(self, gtkspinbutton, data=None):
        self.on_common_spbtn_value_changed("setterheight", gtkspinbutton, data)

        self.halcomp["setterheight"] = gtkspinbutton.get_value()
        self.prefs.putpref("setterheight", gtkspinbutton.get_value(), float)
        self.vcp_reload()
        c = "TS Height = " + "%.4f" % gtkspinbutton.get_value()
        i = self.buffer.get_end_iter()                                                                    # TODO update this code like add_history/self.display_result ??
        if i.get_line() > 1000:
            i.backward_line()
            self.buffer.delete(i, self.buffer.get_end_iter())
        i.set_line(0)
        self.buffer.insert(i, "%s \n" % c)

    # Spinbox for block height with autosave value inside machine pref file
    def on_spbtn_block_height_key_press_event(self, gtkspinbutton, data=None):
        self.on_common_spbtn_key_press_event("blockheight", gtkspinbutton, data)

    def on_spbtn_block_height_value_changed(self, gtkspinbutton, data=None):
        self.on_common_spbtn_value_changed("blockheight", gtkspinbutton, data)

        blockheight = gtkspinbutton.get_value()
        self.halcomp["blockheight"] = blockheight
        self.prefs.putpref("blockheight", blockheight, float)
        # set coordinate system to new origin
        s = "G10 L2 P0 Z%s" % blockheight                                                                 # think about using or not using if self.halcomp["set_zero"]: for make it optional
        print ("blockheight %s") % blockheight
        if self.gcode(s) == -1:
            return
        self.vcp_reload()
        c = "Workpiece Height = " + "%.4f" % gtkspinbutton.get_value()
        i = self.buffer.get_end_iter()                                                                    # TODO update this code like add_history/self.display_result ??
        if i.get_line() > 1000:
            i.backward_line()
            self.buffer.delete(i, self.buffer.get_end_iter())
        i.set_line(0)
        self.buffer.insert(i, "%s \n" % c)
        
    # Down drill bit to tool setter for measuring it vs table probing result
    def on_btn_tool_lenght_released(self, gtkbutton, data=None):
        # Start psng_tool_lenght.ngc
        if self.ocode("o<psng_tool_lenght> call") == -1:
            return
        a = self.stat.probed_position
        tlres = (float(a[2]) - self.halcomp["setterheight"])
        self.display_result_z(tlres)
        print("tool lenght =", tlres)
        self.add_history(gtkbutton.get_tooltip_text(), "Z", 0, 0, 0, 0, 0, 0, 0, 0, tlres, 0, 0)
        
    # Down probe to tool setter for measuring it vs table probing result
    def on_btn_probe_tool_setter_released(self, gtkbutton, data=None):
        # Start psng_probe_tool_setter.ngc
        if self.ocode("o<psng_probe_tool_setter> call") == -1:
            return
        a = self.stat.probed_position
        tsres = (float(a[2]) - self.halcomp["probedtable"])
        self.display_result_z(tsres)
        print("setterheight =", tsres)
        print("probedtable =", self.halcomp["probedtable"])
        self.spbtn_setter_height.set_value(tsres)
        self.add_history(gtkbutton.get_tooltip_text(), "Z", 0, 0, 0, 0, 0, 0, 0, 0, tsres, 0, 0)

    # Down probe to workpiece for measuring it vs Know tool setter height
    def on_btn_probe_workpiece_released(self, gtkbutton, data=None):
        # Start psng_probe_workpiece.ngc
        if self.ocode("o<psng_probe_workpiece> call") == -1:
            return
        a = self.probed_position_with_offsets()
        pwres = float(a[2])
        self.display_result_z(pwres)
        print("workpiecesheight =", pwres)
        print("setterheight", self.halcomp["setterheight"])
        self.spbtn_block_height.set_value(pwres)                                                                    # this call update automatically the offset for workpiece
        self.add_history(gtkbutton.get_tooltip_text(), "Z", 0, 0, 0, 0, 0, 0, 0, 0, pwres, 0, 0)

    # Down probe to table for measuring it and use for calculate tool setter height and can set G10 L20 Z0 if you tick auto zero
    def on_btn_probe_table_released(self, gtkbutton, data=None):
        # Start psng_probe_table.ngc
        if self.ocode("o<psng_probe_table> call") == -1:
            return
        a = self.stat.probed_position
        ptres = float(a[2])
        self.halcomp["probedtable"] = ptres
        self.display_result_z(ptres)
        print("probedtable =", ptres)
        self.add_history(gtkbutton.get_tooltip_text(), "Z", 0, 0, 0, 0, 0, 0, 0, 0, ptres, 0, 0)
        self.set_zerro("Z", 0, 0, ptres)                                                                  # Using auto zero tickbox

    # TOOL TABLE CREATOR
    # TOOL DIA : use X only for find tool setter center and use only after that more accurate Y center value for determinig tool diameter
    # + TOOL lenght Z and the whole sequence is saved as tooltable for later use
    # IMH this sequence need to be first with probe : first execute psng_down for determinate the table height with toolsetter and think about updating tool setter diameter or probe diameter at same time
    # IMH this sequence need to be done secondly with other tool using button Dia only off course
    # ALL OF THIS NEED TO EDIT TOOL TABLE MANUALLY FOR ADD NEW TOOL AND KNOW DIAMETER
    def on_btn_tool_dia_released(self, gtkbutton, data=None):
        tooltable = self.inifile.find("EMCIO", "TOOL_TABLE")
        if not tooltable:
            print(_("**** auto_tool_measurement ERROR ****"))
            print(
                _(
                    "**** Did not find a toolfile file in [EMCIO] TOOL_TABLE ****"
                )
            )
            sys.exit()
        tooldiameter = self.halcomp["toolchange-diameter"]
        print("tool-number = %f" % self.halcomp["toolchange-number"])
        print("tooldiameter from tooltable =", tooldiameter)
        if self.ocode("o<psng_tool_diameter> call") == -1:
            return
        if self.halcomp["toolchange-number"] == 0:
            print("Please mount a tool and ask M6Tx and check if exist with a correct diameter in the tooltable")
            return
        # show Z result
        a = self.probed_position_with_offsets()
        zres = ((float(a[2])) - self.halcomp["setterheight"])
        self.display_result_z(zres)
        #    print("zres = ", zres)
        self.stat.poll()                                                                   # well it is really needed here

        # move X +
        tmpx = (0.5 * (self.tsdiam + tooldiameter) + self.halcomp["ps_xy_clearance"])
        s = """G91
        G1 X-%f
        G90""" % (tmpx)
        if self.gcode(s) == -1:
            return
        if self.z_clearance_down() == -1:
            return
        # Start psng_xplus.ngc
        if self.ocode("o<psng_xplus> call [1]") == -1:
            return
        # show X result
        a = self.probed_position_with_offsets()
        xpres = float(a[0]) + 0.5 * self.tsdiam
        #    print("xpres = ",xpres)
        # move Z to start point up
        if self.z_clearance_up() == -1:
            return

        # move X -
        tmpx = (self.tsdiam + tooldiameter) + (2*self.halcomp["ps_xy_clearance"])
        s = """G91
        G1 X%f
        G90""" % (tmpx)
        if self.gcode(s) == -1:
            return
        if self.z_clearance_down() == -1:
            return
        # Start psng_xminus.ngc
        if self.ocode("o<psng_xminus> call [1]") == -1:
            return
        # show X result
        a = self.probed_position_with_offsets()
        xmres = float(a[0]) - 0.5 * self.tsdiam
        #    print("xmres = ",xmres)
        self.lenght_x()
        xcres = 0.5 * (xpres + xmres)
        #    print("xcres = ",xcres)
        self.display_result_xc(xcres)
        
        
        # move Z to start point up
        if self.z_clearance_up() == -1:
            return
        # go to the new center of X
        s = "G1 X%f" % xcres
        print("xcenter = ",xcres)
        if self.gcode(s) == -1:
            return


        # move Y +
        tmpy = (0.5 * (self.tsdiam + tooldiameter) + self.halcomp["ps_xy_clearance"])
        s = """G91
        G1 Y-%f
        G90""" % (tmpy)
        if self.gcode(s) == -1:
            return
        if self.z_clearance_down() == -1:
            return
        # Start psng_yplus.ngc
        if self.ocode("o<psng_yplus> call [1]") == -1:
            return
        # show Y result
        a = self.probed_position_with_offsets()
        ypres = float(a[1]) + 0.5 * self.tsdiam
        #    print("ypres = ",ypres)
        # move Z to start point up
        if self.z_clearance_up() == -1:
            return

        # move Y -
        tmpy = (self.tsdiam + tooldiameter) + (2*self.halcomp["ps_xy_clearance"])
        s = """G91
        G1 Y%f
        G90""" % (tmpy)
        if self.gcode(s) == -1:
            return
        if self.z_clearance_down() == -1:
            return
        # Start psng_yminus.ngc
        if self.ocode("o<psng_yminus> call [1]") == -1:
            return
        # show Y result
        a = self.probed_position_with_offsets()
        ymres = float(a[1]) - 0.5 * self.tsdiam
        #    print("ymres = ",ymres)
        self.lenght_y()
        ycres = 0.5 * (ypres + ymres)
        #    print("ycres = ",ycres)
        self.display_result_yc(ycres)
        
        diam = ymres - ypres
        diamofsset = diam + (2*self.tsoffset)
        print("old tooldiameter from tooltable =", tooldiameter)
        print("new tooldiameter measured =", diam)
        print("new tooldiameter compensated set in tootlable =", diamofsset)
        self.display_result_d(diam)
        
        self.stat.poll()                                                                      # well it is really needed here
        self.add_history(
            gtkbutton.get_tooltip_text(),
            "XcYcZD",
            0,
            xcres,
            0,
            0,
            0,
            ycres,
            0,
            0,
            zres,
            diamofsset,
            0,
        )
        s = "G10 L1 P%f R%f" % (self.halcomp["toolchange-number"],(0.5*diamofsset))                # 0.14 seem to be needed for my setter adding the necessary distance for radial triggering probe (0.07mm each direction)
        if self.gcode(s) == -1:
            return
        if self.ocode("o<psng_tool_diameter_end> call") == -1:                                    # replace Z clearence and goto new center Y with return to tool change positon
            return


    # Here we create a manual tool change dialog
    def on_tool_change(self, gtkbutton, data=None):
        change = self.halcomp["toolchange-change"]
        toolnumber = self.halcomp["toolchange-number"]
        toolprepnumber = self.halcomp["toolchange-prep-number"]
        print("tool-number =", toolnumber)
        print("tool_prep_number =", toolprepnumber, change)
        if change:
            # if toolprepnumber = 0 we will get an error because we will not be able to get
            # any tooldescription, so we avoid that case
            if toolprepnumber == 0:
                message = _("Please remove the mounted tool and press OK when done")
            else:
                tooltable = self.inifile.find("EMCIO", "TOOL_TABLE")
                if not tooltable:
                    print(_("**** auto_tool_measurement ERROR ****"))
                    print(
                        _(
                            "**** Did not find a toolfile file in [EMCIO] TOOL_TABLE ****"
                        )
                    )
                    sys.exit()
                CONFIGPATH = os.environ["CONFIG_DIR"]
                toolfile = os.path.join(CONFIGPATH, tooltable)
                self.tooledit1.set_filename(toolfile)
                tooldescr = self.tooledit1.get_toolinfo(toolprepnumber)[16]
                message = _(
                    "Please change to tool\n\n# {0:d}     {1}\n\n then click OK."
                ).format(toolprepnumber, tooldescr)
            result = self.warning_dialog(message, title=_("Manual Toolchange"))
            if result:
                self.halcomp["toolchange-changed"] = True
            else:
                print(
                    "toolchange abort",
                    toolnumber,
                    self.halcomp["toolchange-prep-number"],
                )
                self.command.abort()
                self.halcomp["toolchange-prep-number"] = toolnumber
                self.halcomp["toolchange-change"] = False  # Is there any reason to do this to input pin ?
                self.halcomp["toolchange-changed"] = True
                self.warning_dialog(message)
        else:
            self.halcomp["toolchange-changed"] = False
