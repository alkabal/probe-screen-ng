#!/usr/bin/env python
#
# Copyright (c) 2015 Serguei Glavatski ( verser  from cnc-club.ru )
# Copyright (c) 2020 Probe Screen NG Developers
# Copyright (c) 2021 Alkabal free fr with different approach
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
        self.btn_tool_dia = self.builder.get_object("btn_tool_dia")
        self.btn_tool_length = self.builder.get_object("btn_tool_length")
        self.tooledit1 = self.builder.get_object("tooledit1")
        self.chk_use_tool_measurement = self.builder.get_object(
            "chk_use_tool_measurement"
        )

        self.chk_use_tool_measurement.set_active(
            self.prefs.getpref("use_tool_measurement", False, bool)
        )

        self.chk_use_rotate_spindle = self.builder.get_object(
            "chk_use_rotate_spindle"
        )

        # make the pins for tool measurement
        self.halcomp.newpin("use_tool_measurement", hal.HAL_BIT, hal.HAL_OUT)
        self.halcomp.newpin("probedtable", hal.HAL_FLOAT, hal.HAL_OUT)
        self.halcomp.newpin("setterheight", hal.HAL_FLOAT, hal.HAL_OUT)
        self.halcomp.newpin("blockheight", hal.HAL_FLOAT, hal.HAL_OUT)
        # for manual tool change dialog
        self.halcomp.newpin("toolchange-number", hal.HAL_S32, hal.HAL_IN)
        self.halcomp.newpin("toolchange-prep-number", hal.HAL_S32, hal.HAL_IN)
        self.halcomp.newpin("toolchange-changed", hal.HAL_BIT, hal.HAL_OUT)
        pin = self.halcomp.newpin("toolchange-change", hal.HAL_BIT, hal.HAL_IN)
        hal_glib.GPin(pin).connect("value_changed", self.on_tool_change)


        self.halcomp.newpin("toolchange-diameter", hal.HAL_FLOAT, hal.HAL_IN)
        self.halcomp.newpin("use_rotate_spindle", hal.HAL_BIT, hal.HAL_OUT)

        if self.chk_use_tool_measurement.get_active():
            self.halcomp["use_tool_measurement"] = True
            self.hal_led_set_m6.hal_pin.set(1)

        if self.chk_use_rotate_spindle.get_active():
            self.halcomp["use_rotate_spindle"] = True
            self.hal_led_rotate_spindle.hal_pin.set(1)

        self._init_tool_sensor_data()

    # Read the ini file config [TOOLSENSOR] section
    def _init_tool_sensor_data(self):
        xpos = self.inifile.find("TOOLSENSOR", "X")
        ypos = self.inifile.find("TOOLSENSOR", "Y")
        zpos = self.inifile.find("TOOLSENSOR", "Z")
        maxprobe = self.inifile.find("TOOLSENSOR", "MAXPROBE")
        maxprobexy = self.inifile.find("TOOLSENSOR", "MAXPROBE_XY")
        shearchvel = self.inifile.find("TOOLSENSOR", "SEARCH_VEL")
        probevel = self.inifile.find("TOOLSENSOR", "PROBE_VEL")
        tsheight = self.inifile.find("TOOLSENSOR", "HEIGHT")
        zclearance = self.inifile.find("TOOLSENSOR", "Z_CLEARANCE")
        xyclearance = self.inifile.find("TOOLSENSOR", "XY_CLEARANCE")
        latch = self.inifile.find("TOOLSENSOR", "LATCH")
        reverselatch = self.inifile.find("TOOLSENSOR", "REVERSE_LATCH")
        tsdiam = self.inifile.find("TOOLSENSOR", "DIAMETER")
        tsoffset = self.inifile.find("TOOLSENSOR", "DIAM_OFFSET")
        revrott = self.inifile.find("TOOLSENSOR", "REV_ROT_SPEED")
        usepopup = self.inifile.find("PROBE_SCREEN", "TOOLCHANGE_POPUP_STYLE")

        if (
            xpos is None
            or ypos is None
            or zpos is None
            or maxprobe is None
            or maxprobexy is None
            or shearchvel is None
            or probevel is None
            or tsheight is None
            or zclearance is None
            or xyclearance is None
            or latch is None
            or reverselatch is None
            or tsdiam is None
            or tsoffset is None
            or revrott is None
            or usepopup is None
        ):
            self.chk_use_tool_measurement.set_active(False)
            self.frm_probe_pos.set_sensitive(False)

            message   = _("Invalidate TOOLSETTER and REMAP M6")
            secondary = _("Please check the TOOLSENSOR INI configurations")
            self.warning_dialog(message, secondary=secondary)
            return 0
        else:
            self.xpos = float(xpos)
            self.ypos = float(ypos)
            self.zpos = float(zpos)
            self.maxprobe = float(maxprobe)
            self.maxprobexy = float(maxprobexy)
            self.shearchvel = float(shearchvel)
            self.probevel = float(probevel)
            self.tsheight = float(tsheight)
            self.zclearance = float(zclearance)
            self.xyclearance = float(xyclearance)
            self.latch = float(latch)
            self.reverselatch = float(reverselatch)
            self.tsdiam = float(tsdiam)
            self.tsoffset = float(tsoffset)
            self.revrott = float(revrott)
            self.usepopup = float(usepopup)

            #self.spbtn_setter_height.set_value(self.prefs.getpref("setterheight", 0.0, float))
            # at startup read the ini but you can alter the value when machine is running or found the height with probing table + probing setter
            self.spbtn_setter_height.set_value(self.tsheight)
            self.halcomp["setterheight"] = self.spbtn_setter_height.get_value()

            self.spbtn_block_height.set_value(self.prefs.getpref("blockheight", 0.0, float))
            self.halcomp["blockheight"] = self.spbtn_block_height.get_value()


            # to set the hal pin with correct values we emit a toogled
            if self.chk_use_tool_measurement.get_active():
                self.frm_probe_pos.set_sensitive(False)
                self.halcomp["use_tool_measurement"] = True
            else:
                self.frm_probe_pos.set_sensitive(True)
                self.chk_use_tool_measurement.set_sensitive(True)


    def ts_clearance_down(self, data=None):
        # move Z - zclearance
        s = """G91
        G1 Z-%f
        G90""" % (self.zclearance)
        if self.gcode(s) == -1:
            return -1
        return 0

    def ts_clearance_up(self, data=None):
        # move Z + zclearance
        s = """G91
        G1 Z%f
        G90""" % (self.zclearance)
        if self.gcode(s) == -1:
            return -1
        return 0



    # ----------------
    # Remap M6 Buttons
    # ----------------
    # Tickbox from gui for enable disable remap (with saving pref)
    # Logic is now inverted for set.sensitive this is more logic : when remap is enabled you can't change settings so setting to be done before activate remap.
    def on_chk_use_tool_measurement_toggled(self, gtkcheckbutton, data=None):
        if gtkcheckbutton.get_active():
            self.frm_probe_pos.set_sensitive(False)
            self.halcomp["use_tool_measurement"] = True
        else:
            self.frm_probe_pos.set_sensitive(True)
            self.halcomp["use_tool_measurement"] = False
        self.prefs.putpref("use_tool_measurement", gtkcheckbutton.get_active(), bool)
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

        # Record results to history panel
        #c = "TS Height = " + "%.4f" % (gtkspinbutton.get_value())
        self.add_history_text("TS Height = %.4f" % (gtkspinbutton.get_value()))

    # Spinbox for block height with autosave value inside machine pref file
    def on_spbtn_block_height_key_press_event(self, gtkspinbutton, data=None):
        self.on_common_spbtn_key_press_event("blockheight", gtkspinbutton, data)

    def on_spbtn_block_height_value_changed(self, gtkspinbutton, data=None):
        self.on_common_spbtn_value_changed("blockheight", gtkspinbutton, data)
        # set coordinate system to new origin                                      # think about using or not using if self.halcomp["set_zero"]: for make it optional
        if self.gcode("G10 L2 P0 Z%s" % (gtkspinbutton.get_value())) == -1:
            return
        # set coordinate system to new origin
        #if self.gcode("G10 L2 P0 Z%s" % (gtkspinbutton.get_value()))
        #self.vcp_reload()
        # Record results to history panel
        #c = "Workpiece Height = " + "%.4f" % (gtkspinbutton.get_value())
        self.add_history_text("Workpiece Height = %.4f" % (gtkspinbutton.get_value()))

    # Down probe to table for measuring it and use for calculate tool setter height and can set G10 L20 Z0 if you tick auto zero
    @ProbeScreenBase.ensure_errors_dismissed
    def on_btn_probe_table_released(self, gtkbutton, data=None):
        if self.ocode("o<backup_status> call") == -1:
            return
        if self.ocode("o<psng_hook> call [3]") == -1:
            return
        if self.ocode("o<psng_config_check> call") == -1:
            return                # CHECK HAL VALUE FROM GUI FOR CONSITANCY
        # Start psng_probe_table.ngc
        if self.ocode("o<psng_probe_table> call") == -1:
            return
        a = self.stat.probed_position
        ptres = float(a[2])
        self.halcomp["probedtable"] = ptres
        print("probedtable =", ptres)
        self.add_history(
            gtkbutton.get_tooltip_text(),
            "Z",
            z=ptres,
        )
        self.set_zerro("Z", 0, 0, ptres)                                         # Using auto zero tickbox
        if self.ocode("o<backup_restore> call [999] call") == -1:
            return

    # Down probe to tool setter for measuring it vs table probing result
    @ProbeScreenBase.ensure_errors_dismissed
    def on_btn_probe_tool_setter_released(self, gtkbutton, data=None):
        if self.ocode("o<backup_status> call") == -1:
            return
        if self.ocode("o<psng_hook> call [4]") == -1:
            return
        if self.ocode("o<psng_config_check> call") == -1:
            return                # CHECK HAL VALUE FROM GUI FOR CONSITANCY
        # Start psng_probe_setter.ngc
        if self.ocode("o<psng_probe_setter> call") == -1:
            return
        a = self.stat.probed_position
        tsres = (float(a[2]) - self.halcomp["probedtable"])
        print("setterheight =", tsres)
        print("probedtable =", self.halcomp["probedtable"])
        self.spbtn_setter_height.set_value(tsres)
        self.add_history(
            gtkbutton.get_tooltip_text(),
            "Z",
            z=tsres,
        )
        if self.ocode("o<backup_restore> call [999] call") == -1:
            return

    # Down probe to workpiece for measuring it vs Know tool setter height
    @ProbeScreenBase.ensure_errors_dismissed
    def on_btn_probe_workpiece_released(self, gtkbutton, data=None):
        if self.ocode("o<backup_status> call") == -1:
            return
        if self.ocode("o<psng_hook> call [5]") == -1:
            return
        if self.ocode("o<psng_config_check> call") == -1:
            return                # CHECK HAL VALUE FROM GUI FOR CONSITANCY
        # Start psng_probe_workpiece.ngc
        if self.ocode("o<psng_probe_workpiece> call") == -1:
            return
        a = self.probed_position_with_offsets()
        pwres = float(a[2])
        print("workpiecesheight =", pwres)
        print("setterheight", self.halcomp["setterheight"])
        self.spbtn_block_height.set_value(pwres)                                           # this call update automatically the offset for workpiece
        self.add_history(
            gtkbutton.get_tooltip_text(),
            "Z",
            z=pwres,
        )
        if self.ocode("o<backup_restore> call [999] call") == -1:
            return

    # Down drill bit to tool setter for measuring it vs table probing result
    @ProbeScreenBase.ensure_errors_dismissed
    def on_btn_tool_length_released(self, gtkbutton, data=None):
        tooltable = self.inifile.find("EMCIO", "TOOL_TABLE")
        if not tooltable:
            message   = _("Tool Measurement Error")
            secondary = _("Did not find a toolfile file in [EMCIO] TOOL_TABLE")
            self.error_dialog(message, secondary=secondary)
            return
        if self.ocode("o<backup_status> call") == -1:
            return
        if self.ocode("o<psng_hook> call [6]") == -1:
            return
        # Start psng_tool_length.ngc                  # o<psng_config_check> call IS NOT WANTED HERE DUE TO USE INI SETTING
        if self.ocode("o<psng_tool_length> call") == -1:
            return
        a = self.stat.probed_position
        tlres = (float(a[2]) - self.halcomp["setterheight"])
        print("tool length =", tlres)
        self.add_history(
            gtkbutton.get_tooltip_text(),
            "Z",
            z=tlres,
        )
        if self.ocode("o<backup_restore> call [999]") == -1:
            return

    # TOOL TABLE CREATOR
    # TOOL DIA : use X only for find tool setter center and use only after that more accurate Y center value for determinig tool diameter
    # + TOOL length Z and the whole sequence is saved as tooltable for later use
    # IMH this sequence need to be first with probe : first execute psng_down for determinate the table height with toolsetter and think about updating tool setter diameter or probe diameter at same time
    # IMH this sequence need to be done secondly with other tool using button Dia only off course
    # ALL OF THIS NEED TO EDIT TOOL TABLE MANUALLY FOR ADD NEW TOOL AND KNOW DIAMETER
    @ProbeScreenBase.ensure_errors_dismissed
    def on_btn_tool_dia_released(self, gtkbutton, data=None):
        tooltable = self.inifile.find("EMCIO", "TOOL_TABLE")
        if not tooltable:
            message   = _("Tool Measurement Error")
            secondary = _("Did not find a toolfile file in [EMCIO] TOOL_TABLE")
            self.error_dialog(message, secondary=secondary)
            return
        toolnumber = self.halcomp["toolchange-number"]
        tooldiameter = self.halcomp["toolchange-diameter"]
        print("tool-number = %f" % (self.halcomp["toolchange-number"]))
        print("tooldiameter from tooltable =", tooldiameter)

        if self.ocode("o<backup_status> call") == -1:
            return
        if self.ocode("o<psng_hook> call [2]") == -1:
            return
        # Start psng_tool_diameter.ngc                  # o<psng_config_check> call IS NOT WANTED HERE DUE TO USE INI SETTING
        if self.ocode("o<psng_tool_diameter> call") == -1:
            return

        # show Z result
        a = self.probed_position_with_offsets()
        zres = ((float(a[2])) - self.halcomp["setterheight"])

        # move X +
        tmpx = (0.5 * (self.tsdiam + tooldiameter) + self.xyclearance)
        s = """G91
        G1 X-%f
        G90""" % (tmpx)
        if self.gcode(s) == -1:
            return

        if self.ocode("o<psng_tool_diameter_check> call") == -1:
            message   = _("TOOL DIAMETER MEASUREMENT STOPPED")
            self.error_dialog(message)
            return

        if self.ts_clearance_down() == -1:
            return
        # Start psng_xplus.ngc
        if self.ocode("o<psng_start_xplus_probing> call") == -1:
            return
        # show X result
        a = self.probed_position_with_offsets()
        xpres = float(a[0]) + 0.5 * self.tsdiam
        #    print("xpres = ",xpres)
        # move Z to start point up
        if self.ts_clearance_up() == -1:
            return

        # move X -
        tmpx = (self.tsdiam + tooldiameter) + (2*self.xyclearance)
        s = """G91
        G1 X%f
        G90""" % (tmpx)
        if self.gcode(s) == -1:
            return
        if self.ts_clearance_down() == -1:
            return
        # Start psng_xminus.ngc
        if self.ocode("o<psng_start_xminus_probing> call") == -1:
            return
        # show X result
        a = self.probed_position_with_offsets()
        xmres = float(a[0]) - 0.5 * self.tsdiam
        #    print("xmres = ",xmres)
        self.length_x()
        xcres = 0.5 * (xpres + xmres)


        # move Z to start point up
        if self.ts_clearance_up() == -1:
            return
        # go to the new center of X
        s = "G1 X%f" % (xcres)
        print("xcenter = ",xcres)
        if self.gcode(s) == -1:
            return


        # move Y +
        tmpy = (0.5 * (self.tsdiam + tooldiameter) + self.xyclearance)
        s = """G91
        G1 Y-%f
        G90""" % (tmpy)
        if self.gcode(s) == -1:
            return
        if self.ts_clearance_down() == -1:
            return
        # Start psng_yplus.ngc
        if self.ocode("o<psng_start_yplus_probing> call") == -1:
            return
        # show Y result
        a = self.probed_position_with_offsets()
        ypres = float(a[1]) + 0.5 * self.tsdiam
        print("simple probed pos Y+ = ",self.stat.probed_position)
        print("ypres = ",ypres)
        # move Z to start point up
        if self.ts_clearance_up() == -1:
            return

        # move Y -
        tmpy = (self.tsdiam + tooldiameter) + (2*self.xyclearance)
        s = """G91
        G1 Y%f
        G90""" % (tmpy)
        if self.gcode(s) == -1:
            return
        if self.ts_clearance_down() == -1:
            return
        # Start psng_yminus.ngc
        if self.ocode("o<psng_start_yminus_probing> call") == -1:
            return
        # show Y result
        a = self.probed_position_with_offsets()
        ymres = float(a[1]) - 0.5 * self.tsdiam
        print("simple probed pos Y- = ", self.stat.probed_position)
        print("ymres = ",ymres)
        self.length_y()
        ycres = 0.5 * (ypres + ymres)
        print("ycres = ",ycres)

        diam = ymres - ypres
        diamwithofsset = diam + (2*self.tsoffset)
        self.add_history_text("old tooldiameter from tooltable = %.4f" % (tooldiameter))
        self.add_history_text("new tooldiameter measured = %.4f" % (diam))
        self.add_history_text("new tooldiameter compensated set in tootlable = %.4f" % (diamwithofsset))

        self.add_history(
            gtkbutton.get_tooltip_text(),
            "XcYcZD",
            xc=xcres,
            yc=ycres,
            z=zres,
            d=diamwithofsset,
        )
        s = "G10 L1 P%f R%f" % (self.halcomp["toolchange-number"],(0.5*diamwithofsset))           # 0.14 seem to be needed for my setter adding the necessary distance for radial triggering probe (0.07mm each direction)
        if self.gcode(s) == -1:
            return
        if self.ocode("o<psng_tool_diameter_end> call") == -1:                          # replace Z clearence and goto new center Y with return to tool change positon
            return
        if self.ocode("o<backup_restore> call [999]") == -1:
            return


    # Here we create a manual tool change dialog
    def on_tool_change(self, gtkbutton, data=None):
        change = self.halcomp["toolchange-change"]
        toolnumber = self.halcomp["toolchange-number"]
        toolprepnumber = self.halcomp["toolchange-prep-number"]
        self.add_history_text("tool-number = %.4f" % (toolnumber))
        self.add_history_text("tool_prep_number = %.4f" % (toolprepnumber))
        if self.usepopup == 0:
                 result = 0

# One issue need to be corrected if you ask the same tool as actual tool probe start without any confirmation (patched in ocode with M0)

        print("test 1")
        if change:
            print("test 2")
            # if toolprepnumber = 0 we will get an error because we will not be able to get
            # any tooldescription, so we avoid that case
            if toolprepnumber == 0:
                if self.usepopup == 0:
                      result = 1
                elif self.usepopup == 1:
                      message   = _("Please remove the mounted tool and press OK when done or CLOSE popup for cancel")
                      self.warning_dialog(message, title=_("PSNG Manual Toolchange"))
            else:
                tooltable = self.inifile.find("EMCIO", "TOOL_TABLE")
                if not tooltable:
                    message   = _("Tool Measurement Error")
                    secondary = _("Did not find a toolfile file in [EMCIO] TOOL_TABLE")
                    self.error_dialog(message, secondary=secondary, title=_("PSNG Manual Toolchange"))
                    return
                CONFIGPATH = os.environ["CONFIG_DIR"]
                toolfile = os.path.join(CONFIGPATH, tooltable)
                self.tooledit1.set_filename(toolfile)
                tooldescr = self.tooledit1.get_toolinfo(toolprepnumber)[16]
                if self.usepopup == 0:
                      result = 1
                elif self.usepopup == 1:
                      message = _(
                          "Please change to tool\n\n# {0:d}     {1}\n\n then click OK or CLOSE popup for cancel"
                      ).format(toolprepnumber, tooldescr)

            if self.usepopup == 1:
                 result = self.warning_dialog(message, title=_("PSNG Manual Toolchange"))
            if result:
                #self.vcp_reload()                                     # DO NOT DO THAT OR AUTOLENGHT IS KILLED
                self.add_history_text("TOOLCHANGED CORRECTLY")
                self.halcomp["toolchange-changed"] = True
            else:
                self.halcomp["toolchange-prep-number"] = toolnumber
                self.halcomp["toolchange-change"] = False  # Is there any reason to do this to input pin ?
                self.halcomp["toolchange-changed"] = True
                message = _("TOOLCHANGE ABORTED")
                self.error_dialog(message, title=_("PSNG Manual Toolchange"))
        else:
            print("test 3")
            self.halcomp["toolchange-changed"] = False
