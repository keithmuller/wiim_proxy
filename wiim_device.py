#!/usr/bin/env python3

import requests
import json
import urllib3

urllib3.disable_warnings()

class WiimDevice:
    def __init__(self, ip, verbose=0):
        self.ip = ip
        self.verbose = verbose

    # Send the command to the wiim device

    def run_command(self, command):
        url = "https://%s/httpapi.asp?command=%s" % (self.ip, command)
        response = requests.get(url, verify=False)
        if self.verbose == 1:
            print("API command: {0}".format(command))
        if self.verbose == 2:
            print("API command: {0}, got {1}".format(command, response.text))
        return response.text

    # Get Current Status

    def get_player_status(self):
        text = self.run_command("getPlayerStatus")
        data = json.loads(text)
        return data

    # Change input

    def set_line_in(self):
        self.run_command("setPlayerCmd:switchmode:line-in")

    def set_optical_in(self):
        self.run_command("setPlayerCmd:switchmode:optical")

    def set_wifi_in(self):
        self.run_command("setPlayerCmd:switchmode:wifi")

    def set_hdmi_in(self):
        self.run_command("setPlayerCmd:switchmode:HDMI")

    def set_phono_in(self):
        self.run_command("setPlayerCmd:switchmode:phono")

    def set_bluetooth_in(self):
        self.run_command("setPlayerCmd:switchmode:bluetooth")

    # mimic the step input button on the remote
    # you can edit this list to only step through the inputs you have connected
    # Mode values:
    #            10: Ethernet/wifi
    #            41: Bluetooth
    #            49: HDMI
    #            40: Line In (AUX)
    #            43: Optical In
    #            54: Phono In

    def next_input(self):
        # Next input command table: current input: switch to next input
        switch_dict = {
            10: self.set_bluetooth_in,
            41: self.set_hdmi_in,
            49: self.set_line_in,
            40: self.set_wifi_in
        }
        status = self.get_player_status()
        mode = int(status["mode"])

        # Step to next input, if not specified in dict, go to wifi/ethernet
        switch_dict.get(mode, self.set_wifi_in)()

    # Change output

    def set_opt_out(self):
        self.run_command("setAudioOutputHardwareMode:1")

    def set_line_out(self):
        self.run_command("setAudioOutputHardwareMode:2")

    def set_coax_out(self):
        self.run_command("setAudioOutputHardwareMode:3")

    def set_headphone_out(self):
        self.run_command("setAudioOutputHardwareMode:4")

    def set_bluetooth_out(self):
        self.run_command("setAudioOutputHardwareMode:5")

    def set_dlna_out(self):
        self.run_command("setAudioOutputHardwareMode:6")

    # Media controls

    def media_play(self):
        self.run_command("setPlayerCmd:play")

    def media_play_url(self, url):
        self.run_command("setPlayerCmd:play:{0}".format(url))

    def media_pause(self):
        self.run_command("setPlayerCmd:pause")

    def media_resume(self):
        self.run_command("setPlayerCmd:resume")

    def media_stop(self):
        self.run_command("setPlayerCmd:stop")

    def media_toggle(self):
        self.run_command("setPlayerCmd:onepause")

    def media_prev(self):
        self.run_command("setPlayerCmd:prev")

    def media_next(self):
        self.run_command("setPlayerCmd:next")

    def media_set_position(self, position):
        # has the side effect of resuming playback if paused
        position = int(position)
        self.run_command("setPlayerCmd:seek:{0}".format(position))

    def media_seek_fow(self, step):
        self.media_pause()
        status = self.get_player_status()
        totlen = int(status["totlen"]) / 1000
        if totlen <= 0:
            return
        curpos = (int(status["offset_pts"]) / 1000) + step
        self.media_set_position(max(0, min(totlen, curpos)))

    def media_seek_back(self, step):
        self.media_pause()
        status = self.get_player_status()
        totlen = int(status["totlen"]) / 1000
        if totlen <= 0:
            return
        curpos = (int(status["offset_pts"]) / 1000) - step
        self.media_set_position(max(0, min(totlen, curpos)))

    # Volume up and down

    def get_volume(self):
        status = self.get_player_status()
        return status["vol"]

    def set_volume(self, volume):
        volume = int(volume)
        volume = max(0,min(100,volume))
        self.run_command("setPlayerCmd:vol:{0}".format(volume))

    def volume_up(self, step):
        volume = int(self.get_volume())
        self.set_volume(volume + step)

    def volume_down(self, step):
        volume = int(self.get_volume())
        self.set_volume(volume - step)

    # Mute the volume

    def mute_on(self):
        self.run_command("setPlayerCmd:mute:1")

    def mute_off(self):
        self.run_command("setPlayerCmd:mute:0")

    def mute_toggle(self):
        status = self.get_player_status()
        muted = status["mute"] == "1"
        if (muted):
            self.mute_off()
        else:
            self.mute_on()

    # LED and Display commands

    def led_off(self):
        self.run_command("LED_SWITCH_SET:0")

    def led_on(self):
        self.run_command("LED_SWITCH_SET:1")

    def display_off(self):
        self.run_command("setLightOperationBrightConfig:{%22disable%22:1}")

    def display_on(self):
        self.run_command("setLightOperationBrightConfig:{%22disable%22:0}")

    # Run a Preset

    def set_preset(self, pre_numb):
        pre_numb = int(pre_numb)
        pre_numb = max(1,min(12,pre_numb))
        self.run_command("MCUKeyShortClick:{0}".format(pre_numb))
