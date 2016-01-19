# -*- coding:utf8 -*-

import io
import sys
import string

class RDPInstance:

    def __init__(self):
        self.data = {}

    def enable_displayconnectionbar(self):
        self.data["displayconnectionbar"] = 'i:1'

    def disable_displayconnectionbar(self):
        self.data["displayconnectionbar"] = 'i:0'

    def enable_redirectprinters(self):
        self.data["redirectprinters"] = 'i:1'

    def disable_redirectprinters(self):
        self.data["redirectprinters"] = 'i:0'

    def enable_redirectclipboard(self):
        self.data["redirectclipboard"] = 'i:1'

    def disable_redirectclipboard(self):
        self.data["redirectclipboard"] = 'i:0'

    def enable_autoreconnection(self):
        self.data["autoreconnection enabled"] = 'i:1'

    def disable_autoreconnection(self):
        self.data["autoreconnection enabled"] = '1:0'

    def set_authentication_level(self, level):
        self.data["authentication level"] = 'i:%s' % level

    def set_full_address(self, addr):
        self.data["full address"] = 's:%s' % addr

    def set_audiocapturemode(self, mode):
        self.data["audiocapturemode"] = 'i:%s' % mode

    def set_audiomode(self, mode):
        self.data["audiomode"] = 'i:%s' % mode

    def set_keyboardhook(self, hook):
        self.data["keyboardhook"] = 'i:%s' % hook

    def enable_redirectsmartcards(self):
        self.data["redirectsmartcards"] = 'i:1'

    def disable_redirectsmartcards(self):
        self.data["redirectsmartcards"] = 'i:0'

    def enable_redirectcomports(self):
        self.data["redirectcomports"] = 'i:1'

    def disable_redirectcomports(self):
        self.data["redirectcomports"] = 'i:0'

    def enable_drivestoredirect(self, letter, name):
        if "drivestoredirect" not in self.data:
            self.data["drivestoredirect"] = {}
        self.data["drivestoredirect"][letter] = name

    def disable_drivestoredirect(self, letter):
        if "drivestoredirect" not in self.data:
            return
        if letter in self.data["drivestoredirect"]:
            del self.data["drivestoredirect"][letter]

    def set_session_bpp(self, bpp):
        self.data["session bpp"] = 'i:%s' % bpp

    def set_connection_type(self, t):
        self.data["connection type"] = 'i:%s' % t

    def enable_wallpaper(self):
        self.data["disable wallpaper"] = 'i:0'

    def disable_wallpaper(self):
        self.data["disable wallpaper"] = 'i:1'

    def enable_font_smoothing(self):
        self.data["allow font smoothing"] = 'i:1'

    def disable_font_smoothing(self):
        self.data["allow font smoothing"] = 'i:0'

    def enable_desktop_composition(self):
        self.data["allow desktop composition"] = 'i:1'

    def disable_desktop_composition(self):
        self.data["allow desktop composition"] = 'i:0'

    def enable_full_window_drag(self):
        self.data["disable full window drag"] = 'i:0'

    def disable_full_window_drag(self):
        self.data["disable full window drag"] = 'i:1'

    def enable_menu_anims(self):
        self.data["disable menu anims"] = 'i:0'

    def disable_menu_anims(self):
        self.data["disable menu anims"] = 'i:1'

    def enable_themes(self):
        self.data["disable themes"] = 'i:0'

    def disable_themes(self):
        self.data["disable themes"] = 'i:1'

    def enable_bitmapcachepersistenable(self):
        self.data["bitmapcachepersistenable"] = 'i:1'

    def disable_bitmapcachepersistenable(self):
        self.data["bitmapcachepersistenable"] = 'i:0'

    def set_desktopwidth(self, len):
        self.data["desktopwidth"] = 'i:%s' % len

    def set_desktopheight(self, len):
        self.data["desktopheight"] = 'i:%s' % len

    def write(self, file):
        try:
            if isinstance(file, string):
                file = io.open(file, 'w')
        except:
            pass
        for key, value in self.data:
            pass

